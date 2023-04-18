import numpy as np

from . import appconfig
from base64 import b64decode
from cv2 import imread
from diffusers import StableDiffusionPipeline, StableDiffusionUpscalePipeline
from diffusers import StableDiffusionInpaintPipeline
from .image_fns import save_image, resize_image, save_segmented_image
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from torch import float16
from .utils import get_prompt, get_negative_prompt


def generate_image(config):
    inference_pipe = StableDiffusionPipeline.from_pretrained(
            appconfig.IMAGE_MODEL, torch_dtype=float16).to("cuda")

    image = inference_pipe(
        get_prompt(config["prompt"]),
        negative_prompt=get_negative_prompt(
            config["negativePrompt"]),
        num_inference_steps=int(config["inferenceSteps"]),
        guidance_scale=float(config["guidanceScale"])
        ).images[0]

    return {"image_url": save_image(image)}


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

    return {"image_url": save_image(inpainted_image)}


def segment_image(config):
    img = imread(config["image_url"])
    sam = sam_model_registry["vit_h"](checkpoint=appconfig.SEGMENT_MODEL)
    sam.to("cuda")
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(img)
    for item in masks:
        item["segmentation"] = item["segmentation"].tolist()
    save_segmented_image(img, masks)
    return {"image_mask": masks}
