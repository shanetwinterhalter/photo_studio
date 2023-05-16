import replicate
import numpy as np

from . import appconfig
from PIL import Image
from skimage.measure import label, regionprops
from scipy.spatial import distance
from .utils.debug import create_composite_image
from .utils.img_manip import make_square
from .utils.img_ops import (save_image, img_to_bytes, load_image_from_url)
from .utils.masks import create_mask_image


def get_white_blob_bounding_boxes(mask):
    # Convert image into numpy array
    mask_np = np.array(mask.convert('L'))

    # Perform CCA on the mask
    labeled_mask, _ = label(mask_np, connectivity=2, return_num=True)

    # Get properties of labeled regions
    regions = regionprops(labeled_mask)

    # Get the bounding boxes of the blobs and calculate their areas
    bounding_boxes = [
        (region.bbox, region.centroid)
        for region in regions if region.area >= 1]

    # Calculate the center of the image
    image_center = (mask_np.shape[0] // 2, mask_np.shape[1] // 2)

    # Sort the bounding boxes in descending order of their
    # distance from the center
    bounding_boxes.sort(
        key=lambda x: distance.euclidean(image_center, x[1]), reverse=True)

    # Extract just the bounding boxes from the sorted list
    bounding_boxes = [bbox for bbox, _ in bounding_boxes]

    return bounding_boxes


def get_image_sections_from_bounding_boxes(
        image,
        bounding_boxes,
        section_size=512
        ):
    sections = []
    image_width, image_height = image.size

    # If image smaller than section, just pass whole image
    if image_width < section_size and image_height < section_size:
        return [(0, 0, 0, 0)]
    # Attempting to handle situations where one dim > 512 and another <512
    # TODO: Test this, not sure how well it will work
    elif not (image_width > section_size and image_height > section_size):
        image, padding = make_square(image)

    # Initialize a binary mask to keep track of covered areas
    covered_area = np.zeros((image_height, image_width), dtype=bool)

    # Calculate the center of the image
    center_x = image_width / 2
    center_y = image_height / 2

    for bbox in bounding_boxes:
        minr, minc, maxr, maxc = bbox
        # Check if this bbox is already covered by another section
        if np.all(covered_area[minr:maxr, minc:maxc]):
            continue

        height = maxr - minr
        width = maxc - minc

        # Determine the corner of the bounding box that is farthest from
        # the center of the image
        if minr < center_y:
            start_r = minr
        else:
            start_r = minr + height - section_size
        if minc < center_x:
            start_c = minc
        else:
            start_c = minc + width - section_size

        # Calculate number of sections and spacing between them
        n_width_sections = width // section_size + 1
        n_height_sections = height // section_size + 1
        width_offset = section_size - (
            (section_size * n_width_sections - width) //
            (n_width_sections - 1)) if n_width_sections != 1 else 0
        height_offset = section_size - (
            (section_size * n_height_sections - height) //
            (n_height_sections - 1)) if n_width_sections != 1 else 0

        for v in range(n_width_sections):
            start_x = start_c + v * width_offset
            # Ensure no sections go outside image
            if start_x < 0:
                start_x = 0

            end_x = start_x + section_size
            # Ensure no sections go outside image
            if end_x > image_width:
                end_x = image_width
                start_x = end_x - section_size

            for h in range(n_height_sections):
                start_y = start_r + h * height_offset
                if start_y < 0:
                    start_y = 0

                end_y = start_y + section_size
                if end_y > image_height:
                    end_y = image_height
                    start_y = end_y - section_size

                section = (
                    start_y,
                    start_x,
                    end_y,
                    end_x
                )
                sections.append(section)
                covered_area[start_y:end_y, start_x:end_x] = True

    return sections


def preprocess_image(init_img, mask_img, subimage_size=512):
    bounding_boxes = get_white_blob_bounding_boxes(mask_img)
    section_boundaries = get_image_sections_from_bounding_boxes(
        init_img, bounding_boxes, subimage_size)
    return section_boundaries


def inpaint_image(config):
    model = appconfig.INPAINT_MODEL["modelName"] + \
            ":" + appconfig.INPAINT_MODEL["modelVersion"]

    init_img = Image.open(config["image_url"]).convert("RGB")
    output_image = init_img.copy()
    mask_img = create_mask_image(config["mask"], init_img.size)

    inpaint_sections = preprocess_image(init_img, mask_img,
                                        appconfig.GRID_SIZE)

    for (minr, minc, maxr, maxc) in inpaint_sections:
        section_position = (minc, minr, maxc, maxr)
        section = init_img.crop(section_position)
        mask_section = mask_img.crop(section_position)
        output = replicate.run(
            model,
            input={
                "prompt": config["prompt"],
                "negative_prompt": config["negativePrompt"],
                "image": img_to_bytes(section),
                "mask": img_to_bytes(mask_section),
                "num_outputs": appconfig.IMAGE_MODEL["numOutputs"],
                "num_inference_steps": int(config["inferenceSteps"]),
                "guidance_scale": float(config["guidanceScale"])
            }
        )
        inpainted_section = load_image_from_url(output[0])
        output_image.paste(inpainted_section, section_position)

    local_img_url = save_image(output_image)

    if appconfig.DEBUG_MODE:
        save_image(mask_img, "mask_image.png", debug=True)
        save_image(init_img, "initial_image.png", debug=True)
        save_image(output_image, "inpainted_image.png", debug=True)
        composite_image = create_composite_image(
            init_img, mask_img,
            bounding_boxes=get_white_blob_bounding_boxes(mask_img),
            section_boxes=inpaint_sections)
        save_image(composite_image, "composite_image.png", debug=True)
        for idx, (minr, minc, maxr, maxc) in enumerate(inpaint_sections):
            section_position = (minc, minr, maxc, maxr)
            save_image(init_img.crop(section_position), str(idx) +
                       "section_img.png", debug=True)
            save_image(mask_img.crop(section_position), str(idx) +
                       "section_mask.png", debug=True)

    return {"image_url": local_img_url}
