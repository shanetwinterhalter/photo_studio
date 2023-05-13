import replicate

from . import appconfig
from PIL import Image
from .utils.img_manip import make_square
from .utils.img_ops import save_image, save_image_from_url, img_to_bytes
from .utils.masks import create_mask_image


def inpaint_image(config):
    model = appconfig.INPAINT_MODEL["modelName"] + \
            ":" + appconfig.INPAINT_MODEL["modelVersion"]

    init_img = Image.open(config["image_url"]).convert("RGB")
    mask_img = create_mask_image(config["mask"], init_img.size)

    # Add padding to ensure images are square
    init_img, padding = make_square(init_img)
    mask_img, _ = make_square(mask_img)

    # Scale padding - inpaint always returns 512x512
    scale_factor = 512 / init_img.size[0]
    padding = tuple(pad * scale_factor for pad in padding)

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
    local_img_url = save_image_from_url(output[0], padding=padding)

    if appconfig.DEBUG_MODE:
        save_image(mask_img, "mask_image.png", debug=True)
        save_image(init_img, "initial_image.png", debug=True)
        save_image(Image.open(local_img_url),
                   "inpainted_image.png",
                   debug=True)

    return {"image_url": local_img_url}
