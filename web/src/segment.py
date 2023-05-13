import replicate

from . import appconfig
from PIL import Image
from .utils.img_ops import img_to_bytes, save_image_from_url


def segment_image(config):
    if not appconfig.ENABLE_SEGMENTATION:
        return {"image_mask": None}

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

    mask_image_paths = []
    for idx, item in enumerate(output):
        mask_filename = original_filename + "_" + str(idx) + ".png"
        mask_url = save_image_from_url(item, filename=mask_filename)
        mask_image_paths.append(mask_url)

    if appconfig.DEBUG_MODE:
        for idx, item in enumerate(output):
            debug_mask_filename = "seg_mask_" + str(idx) + ".png"
            save_image_from_url(item, filename=debug_mask_filename, debug=True)

    return {"image_mask": mask_image_paths}
