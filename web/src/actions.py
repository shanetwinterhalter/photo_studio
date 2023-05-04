import numpy as np
import replicate

from . import appconfig
from base64 import b64decode
from diffusers import StableDiffusionUpscalePipeline, StableDiffusionInpaintPipeline
from .image_fns import save_image, resize_image, save_segmented_image, save_image_from_url
from io import BytesIO
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from torch import float16
from .utils import get_prompt, get_negative_prompt


def generate_image(config):
    model = appconfig.IMAGE_MODEL["modelName"] + \
            ":" + appconfig.IMAGE_MODEL["modelVersion"]
    output = replicate.run(
        model,
        input={
            "prompt": config["prompt"],
            "negative_prompt": config["negativePrompt"],
            "image_dimensions": appconfig.IMAGE_MODEL["dimensions"],
            "num_outputs": appconfig.IMAGE_MODEL["numOutputs"],
            "num_inference_steps": int(config["inferenceSteps"]),
            "guidance_scale": float(config["guidanceScale"]),
            "scheduler": appconfig.IMAGE_MODEL["scheduler"]
        }
    )
    # We can support multiple images easily but for now limit to 1
    local_img_url = save_image_from_url(output[0])
    return {"image_url": local_img_url}


def upscale_image(config):
    upscale_pipeline = StableDiffusionUpscalePipeline.from_pretrained(
        appconfig.UPSCALE_MODEL, torch_dtype=float16).to("cuda")
    upscale_pipeline.enable_xformers_memory_efficient_attention()

    init_img = Image.open(config["image_url"]).convert("RGB")
    init_img = init_img.resize(appconfig.UPSCALE_RES)

    upscaled_image = upscale_pipeline(
        prompt=get_prompt(config["prompt"]),
        image=init_img,
        negative_prompt=get_negative_prompt(
            config["negativePrompt"]),
        num_inference_steps=int(config["inferenceSteps"]),
        guidance_scale=float(config["guidanceScale"])
    ).images[0]

    return {"image_url": save_image(upscaled_image)}


def inpaint_image(config):
    inpainting_pipeline = \
        StableDiffusionInpaintPipeline.from_pretrained(
            appconfig.INPAINT_MODEL, torch_dtype=float16).to("cuda")
    inpainting_pipeline.enable_xformers_memory_efficient_attention()

    init_img = Image.open(config["image_url"]).convert("RGB")
    decoded_mask = b64decode(config["mask"])
    height, width = init_img.size
    mask_array = np.frombuffer(decoded_mask, dtype=np.uint8)
    mask_array = mask_array.reshape(width, height) * 255
    mask_img = Image.fromarray(mask_array).convert("RGB")
    init_img = resize_image(init_img, appconfig.MAX_INPAINT_RES)
    mask_img = mask_img.resize(init_img.size)
    save_image(mask_img, "mask_image.jpeg", debug=True)
    save_image(init_img, "initial_image.jpeg", debug=True)

    inpainted_image = inpainting_pipeline(
        prompt=get_prompt(config["prompt"]),
        height=init_img.size[1],
        width=init_img.size[0],
        image=init_img,
        mask_image=mask_img,
        negative_prompt=get_negative_prompt(
            config["negativePrompt"]),
        num_inference_steps=int(config["inferenceSteps"]),
        guidance_scale=float(config["guidanceScale"])
    ).images[0]
    save_image(inpainted_image, "inpainted_image.jpeg", debug=True)
    return {"image_url": save_image(inpainted_image)}


def segment_image(config):
    img = Image.open(config["image_url"])
    # max_width, max_height = appconfig.MAX_SEGMENT_RES
    # img_width, img_height = img.size

    # if img_width > max_width or img_height > max_height:
    #    aspect_ratio = float(img_width) / float(img_height)
    #    if img_width > img_height:
    #        new_width = max_width
    #        new_height = int(new_width / aspect_ratio)
    #    else:
    #        new_height = max_height
    #        new_width = int(new_height * aspect_ratio)
    #    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    img_array = np.array(img)
    sam = sam_model_registry["vit_h"](checkpoint=appconfig.SEGMENT_MODEL)
    sam.to("cuda")
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(img_array)
    for item in masks:
        item["segmentation"] = item["segmentation"].tolist()
    save_segmented_image(img_array, masks, "segmented_image.jpeg", debug=True)
    return {"image_mask": masks}


def upload_image(config):
    image_data = BytesIO(b64decode(config["image"].split(",")[1]))
    image = Image.open(image_data).convert('RGB')
    return {"image_url": save_image(image)}
