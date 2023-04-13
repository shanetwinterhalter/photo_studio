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
import io
import json
import numpy as np

import time


IMAGE_MODEL = "../models/shane9r"
SEGMENT_MODEL = "../models/sam_vit_h_4b8939.pth"
NEGATIVE_PROMPT = "bad, deformed, ugly, bad anatomy, cartoon, animated," + \
                "scary, wrinkles, duplicate, double"
NUM_INFERENCE_STEPS = 15
GUIDANCE_SCALE = 20

UPSCALE_MODEL = "stabilityai/stable-diffusion-x4-upscaler"
UPSCALE_RES = (256, 256)
UPSCALING_INFERENCE_STEPS = 15

INPAINT_MODEL = "stabilityai/stable-diffusion-2-inpainting"
INPAINTING_INFERENCE_STEPS = 15
INPAINTING_GUIDANCE_SCALE = 7.5
INPAINT_RES = (512, 512)


app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = 'images'
app.config["MAX_IMAGE_AGE_HOURS"] = 24


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


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main_page.html')


@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.form["prompt"]
    inference_pipe = StableDiffusionPipeline.from_pretrained(
            IMAGE_MODEL, torch_dtype=torch.float16).to("cuda")
    image = inference_pipe(
        prompt,
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=NUM_INFERENCE_STEPS,
        guidance_scale=GUIDANCE_SCALE
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
        prompt="",
        image=init_img,
        num_inference_steps=UPSCALING_INFERENCE_STEPS,
        negative_prompt=NEGATIVE_PROMPT
    ).images[0]
    return jsonify({"image_url": save_image(upscaled_image)})


@app.route('/inpaint_image', methods=['POST'])
def inpaint_image():
    inpainting_pipeline = StableDiffusionInpaintPipeline.from_pretrained(
        INPAINT_MODEL, torch_dtype=torch.float16).to("cuda")
    inpainting_pipeline.enable_xformers_memory_efficient_attention()

    init_img = Image.open(request.form["image_url"]).convert("RGB")
    decoded_mask = base64.b64decode(request.form["mask"]).decode("utf-8")
    height, width = init_img.size
    mask_array = np.array(json.loads(decoded_mask), dtype=np.uint8)
    mask_array = mask_array.reshape(height, width) * 255
    mask_img = Image.fromarray(mask_array).convert("RGB")

    inpainted_image = inpainting_pipeline(
        prompt="",
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=INPAINTING_INFERENCE_STEPS,
        guidance_scale=INPAINTING_GUIDANCE_SCALE,
        height=init_img.size[1],
        width=init_img.size[0],
        image=init_img,  # .resize(INPAINT_RES),
        mask_image=mask_img  # .resize(INPAINT_RES)
    ).images[0]

    return jsonify({"image_url": save_image(inpainted_image)})


@app.route('/segment_image', methods=['POST'])
def segment_image():
    print("Starting image segmentation")
    start_time = time.time()
    img = cv2.imread(request.form["image_url"])
    sam = sam_model_registry["vit_h"](checkpoint=SEGMENT_MODEL)
    sam.to("cuda")
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(img)
    for item in masks:
        item["segmentation"] = item["segmentation"].tolist()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Segmentation complete, it took {elapsed_time:.6f} seconds")
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
