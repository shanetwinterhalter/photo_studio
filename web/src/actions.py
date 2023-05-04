import replicate

from . import appconfig
from base64 import b64decode
from .image_fns import (save_image, save_image_from_url,
                        create_mask_image, img_to_bytes)
from io import BytesIO
from PIL import Image


def upload_image(config):
    image_data = BytesIO(b64decode(config["image"].split(",")[1]))
    image = Image.open(image_data).convert('RGB')
    return {"image_url": save_image(image)}


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

    if appconfig.DEBUG_MODE:
        save_image(Image.open(local_img_url),
                   "generated_image.png",
                   debug=True)

    return {"image_url": local_img_url}


def inpaint_image(config):
    model = appconfig.INPAINT_MODEL["modelName"] + \
            ":" + appconfig.INPAINT_MODEL["modelVersion"]

    init_img = Image.open(config["image_url"]).convert("RGB")
    mask_img = create_mask_image(config["mask"], init_img.size)

    output = replicate.run(
        model,
        input={
            "prompt": config["prompt"],
            "negative_prompt": config["negativePrompt"],
            "image": img_to_bytes(init_img),
            "mask": img_to_bytes(mask_img),
            "num_outputs": appconfig.IMAGE_MODEL["numOutputs"],
            "num_inference_steps": int(config["inferenceSteps"]),
            "guidance_scale": float(config["guidanceScale"])
        }
    )
    # We can support multiple images easily but for now limit to 1
    local_img_url = save_image_from_url(output[0])

    if appconfig.DEBUG_MODE:
        save_image(mask_img, "mask_image.png", debug=True)
        save_image(init_img, "initial_image.png", debug=True)
        save_image(Image.open(local_img_url),
                   "inpainted_image.png",
                   debug=True)

    return {"image_url": local_img_url}


def segment_image(config):
    model = appconfig.SEGMENT_MODEL["modelName"] + \
        ":" + appconfig.SEGMENT_MODEL["modelVersion"]

    original_filename = config["image_url"].split("/")[-1].split(".")[0]
    img = Image.open(config["image_url"]).convert("RGB")

    output = replicate.run(
        model,
        input={
            "image": img_to_bytes(img),
        }
    )

    mask_image_paths = [] * len(output)
    for idx, item in enumerate(output):
        mask_filename = original_filename + "_" + str(idx) + ".png"
        mask_url = save_image_from_url(item, filename=mask_filename)
        mask_image_paths.append(mask_url)

    if appconfig.DEBUG_MODE:
        for idx, item in enumerate(output):
            debug_mask_filename = "seg_mask_" + str(idx) + ".png"
            save_image_from_url(item, filename=debug_mask_filename)

    return {"image_mask": mask_image_paths}
