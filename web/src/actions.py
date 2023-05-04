import numpy as np
import replicate

from . import appconfig
from base64 import b64decode
from .image_fns import (save_image, save_segmented_image,
                        save_image_from_url, create_mask_image)
from io import BytesIO
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry


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

    # Convert the images to bytes in memory
    init_img_bytes = BytesIO()
    mask_img_bytes = BytesIO()
    init_img.save(init_img_bytes, format='PNG')
    mask_img.save(mask_img_bytes, format='PNG')

    # Reset the buffer position to the beginning
    init_img_bytes.seek(0)
    mask_img_bytes.seek(0)

    output = replicate.run(
        model,
        input={
            "prompt": config["prompt"],
            "negative_prompt": config["negativePrompt"],
            "image": init_img_bytes,
            "mask": mask_img_bytes,
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
