import replicate

from . import appconfig
from .utils.img_ops import save_image, save_image_from_url
from PIL import Image


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
