from diffusers import StableDiffusionPipeline, StableDiffusionUpscalePipeline
from diffusers import StableDiffusionInpaintPipeline
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
from hashlib import md5
from datetime import datetime, timedelta
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import cv2
import os
import time
import threading
import torch
import base64
import numpy as np
import random

import time

DEFAULTARGS = {
    "prompt": "a portrait photo of a shane man, handsome, " +
              "clear skin, photograph, photorealistic, well lit",
    "inferenceSteps": "15",
    "guidanceScale": "7.5",
    "negativePrompt": "bad, deformed, ugly, bad anatomy, cartoon, " +
                      "animated, scary, wrinkles, duplicate, double"
}

IMAGE_MODEL = "../models/shane9r"
SEGMENT_MODEL = "../models/sam_vit_h_4b8939.pth"

UPSCALE_MODEL = "stabilityai/stable-diffusion-x4-upscaler"
UPSCALE_RES = (256, 256)

INPAINT_MODEL = "stabilityai/stable-diffusion-2-inpainting"
MAX_INPAINT_RES = (1024, 1024)


app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = 'images'
app.config["MAX_IMAGE_AGE_HOURS"] = 24


def save_segmented_image(image, masks):
    colors = [tuple([random.randint(0, 255) for _ in range(3)]) for _ in range(len(masks))]
    for idx, mask in enumerate(masks):
        mask = np.array(mask['segmentation'], dtype=np.uint8)

        color_mask = np.zeros_like(image)
        color_mask[mask > 0] = colors[idx]
        # Overlay the color mask on the image
        image = cv2.addWeighted(image, 1, color_mask, 0.5, 0)
    # Save the output image
    cv2.imwrite(os.path.join(app.config["IMAGE_UPLOADS"], 'segmented_image.jpg'), image)


def delete_old_files():
    folder_path = app.config["IMAGE_UPLOADS"]
    time_limit = datetime.now() - \
        timedelta(hours=app.config["MAX_IMAGE_AGE_HOURS"])
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))

        if file_mtime < time_limit:
            os.remove(file_path)
            print(f"Deleted old file: {filename}")
    time.sleep(3600)


def save_image(image):
    filename = f"{md5(image.tobytes()).hexdigest()}.jpeg"
    image.save(
        os.path.join(app.config["IMAGE_UPLOADS"], filename),
        'JPEG',
        quality=90
    )
    image_url = f"{app.config['IMAGE_UPLOADS']}/{filename}"
    return image_url


def get_prompt(prompt):
    if prompt:
        return prompt
    else:
        return DEFAULTARGS["prompt"]


def get_negative_prompt(request):
    if request:
        return request
    else:
        return DEFAULTARGS["negativePrompt"]


def resize_image(image, max_res):
    width, height = image.size
    if width > max_res[0] or height > max_res[1]:
        if width > height:
            new_width = max_res[0]
            new_height = int(height * new_width / width)
        else:
            new_height = max_res[1]
            new_width = int(width * new_height / height)
        return image.resize((new_width, new_height))
    else:
        return image


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main_page.html', DEFAULTARGS=DEFAULTARGS)


@app.route('/generate_image', methods=['POST'])
def generate_image():
    inference_pipe = StableDiffusionPipeline.from_pretrained(
            IMAGE_MODEL, torch_dtype=torch.float16).to("cuda")

    image = inference_pipe(
        get_prompt(request.form["prompt"]),
        negative_prompt=get_negative_prompt(request.form["negativePrompt"]),
        num_inference_steps=int(request.form["inferenceSteps"]),
        guidance_scale=float(request.form["guidanceScale"])
        ).images[0]

    return jsonify({"image_url": save_image(image)})


@app.route('/upload_image', methods=['POST'])
def upload_image():
    image = Image.open(request.files["image"].stream).convert('RGB')
    return jsonify({"image_url": save_image(image)})


@app.route('/upscale_image', methods=['POST'])
def upscale_image():
    upscale_pipeline = StableDiffusionUpscalePipeline.from_pretrained(
        UPSCALE_MODEL, torch_dtype=torch.float16).to("cuda")
    upscale_pipeline.enable_xformers_memory_efficient_attention()

    init_img = Image.open(request.form["image_url"]).convert("RGB")
    init_img = init_img.resize(UPSCALE_RES)

    upscaled_image = upscale_pipeline(
        prompt=get_prompt(request.form["prompt"]),
        image=init_img,
        negative_prompt=get_negative_prompt(request.form["negativePrompt"]),
        num_inference_steps=int(request.form["inferenceSteps"]),
        guidance_scale=float(request.form["guidanceScale"])
    ).images[0]
    return jsonify({"image_url": save_image(upscaled_image)})


@app.route('/inpaint_image', methods=['POST'])
def inpaint_image():
    inpainting_pipeline = StableDiffusionInpaintPipeline.from_pretrained(
        INPAINT_MODEL, torch_dtype=torch.float16).to("cuda")
    inpainting_pipeline.enable_xformers_memory_efficient_attention()

    init_img = Image.open(request.form["image_url"]).convert("RGB")
    decoded_mask = base64.b64decode(request.form["mask"])
    height, width = init_img.size
    mask_array = np.frombuffer(decoded_mask, dtype=np.uint8)
    mask_array = mask_array.reshape(width, height) * 255
    mask_img = Image.fromarray(mask_array).convert("RGB")
    init_img = resize_image(init_img, MAX_INPAINT_RES)
    mask_img = mask_img.resize(init_img.size)

    inpainted_image = inpainting_pipeline(
        prompt=get_prompt(request.form["prompt"]),
        height=init_img.size[1],
        width=init_img.size[0],
        image=init_img,
        mask_image=mask_img,
        negative_prompt=get_negative_prompt(request.form["negativePrompt"]),
        num_inference_steps=int(request.form["inferenceSteps"]),
        guidance_scale=float(request.form["guidanceScale"])
    ).images[0]

    return jsonify({"image_url": save_image(inpainted_image)})


@app.route('/segment_image', methods=['POST'])
def segment_image():
    img = cv2.imread(request.form["image_url"])
    sam = sam_model_registry["vit_h"](checkpoint=SEGMENT_MODEL)
    sam.to("cuda")
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(img)
    for item in masks:
        item["segmentation"] = item["segmentation"].tolist()
    save_segmented_image(img, masks)
    return jsonify(
        {"image_mask": masks}
    )


@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)


if __name__ == '__main__':
    file_deletion_thread = threading.Thread(target=delete_old_files,
                                            daemon=True)
    file_deletion_thread.start()
    app.run(debug=True)
