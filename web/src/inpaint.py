import replicate
import numpy as np

from . import appconfig
from PIL import Image, ImageDraw
from skimage.measure import label, regionprops
from scipy.spatial import distance
from .utils.img_ops import save_image, save_image_from_url, img_to_bytes
from .utils.masks import create_mask_image


def get_white_blob_bounding_boxes(mask):
    # Convert image into numpy array
    mask_np = np.array(mask.convert('L'))

    # Perform CCA on the mask
    labeled_mask, _ = label(mask_np, connectivity=2, return_num=True)

    # Get properties of labeled regions
    regions = regionprops(labeled_mask)

    # Get the bounding boxes of the blobs and calculate their areas
    bounding_boxes = [(region.bbox, region.centroid) for region in regions if region.area >= 1]

    # Calculate the center of the image
    image_center = (mask_np.shape[0] // 2, mask_np.shape[1] // 2)

    # Sort the bounding boxes in descending order of their distance from the center
    bounding_boxes.sort(key=lambda x: distance.euclidean(image_center, x[1]), reverse=True)

    # Extract just the bounding boxes from the sorted list
    bounding_boxes = [bbox for bbox, _ in bounding_boxes]

    return bounding_boxes


def get_image_sections_from_bounding_boxes(image, bounding_boxes, section_size=512):
    sections = []
    image_width, image_height = image.size

    # Initialize a binary mask to keep track of covered areas
    covered_area = np.zeros((image_height, image_width), dtype=bool)

    # Calculate the center of the image
    center_x = image_width / 2
    center_y = image_height / 2

    for bbox in bounding_boxes:
        minr, minc, maxr, maxc = bbox
        height = maxr - minr
        width = maxc - minc

        # Determine the corner of the bounding box that is furthest from the center of the image
        if minr < center_y:
            start_r = minr
        else:
            start_r = minr + height - section_size
        if minc < center_x:
            start_c = minc
        else:
            start_c = minc + width - section_size

        end_r = start_r + section_size
        end_c = start_c + section_size

        # Check if this area is already covered
        if not np.all(covered_area[minr:maxr, minc:maxc]):
            section = (start_r, start_c, end_r, end_c)
            sections.append(section)
            # Mark this area as covered
            covered_area[start_r:end_r, start_c:end_c] = True

        if maxr > end_r and not np.all(covered_area[maxr - section_size:maxr, start_c:end_c]):
            sections.append((maxr - section_size, start_c, maxr, end_c))
            covered_area[maxr - section_size:maxr, start_c:end_c] = True
        if maxc > end_c and not np.all(covered_area[start_r:end_r, maxc - section_size:maxc]):
            sections.append((start_r, maxc - section_size, end_r, maxc))
            covered_area[start_r:end_r, maxc - section_size:maxc] = True

    return sections


def get_subimages(init_img, mask_img, subimage_size=512):
    bounding_boxes = get_white_blob_bounding_boxes(mask_img)
    section_boundaries = get_image_sections_from_bounding_boxes(init_img, bounding_boxes, subimage_size)

    # Extract image sections
    inpaint_sections = []
    section_coords = []

    for (minr, minc, maxr, maxc) in section_boundaries:
        section_position = (minc, minr, maxc, maxr)
        section = init_img.crop(section_position)
        mask_section = mask_img.crop(section_position)
        section_coords.append(section_position)
        inpaint_sections.append((section, mask_section))

    return (inpaint_sections, section_coords)


def reassemble_image(init_img, output_urls, inpaint_coords):
    for url, position in zip(output_urls, inpaint_coords):
        img_section = Image.open(url)
        init_img.paste(img_section, position)
    return init_img


def inpaint_image(config):
    model = appconfig.INPAINT_MODEL["modelName"] + \
            ":" + appconfig.INPAINT_MODEL["modelVersion"]

    init_img = Image.open(config["image_url"]).convert("RGB")
    mask_img = create_mask_image(config["mask"], init_img.size)

    inpaint_sections, inpaint_coords = get_subimages(init_img, mask_img, appconfig.GRID_SIZE)

    output_urls = []
    for item in inpaint_sections:
        output = replicate.run(
            model,
            input={
                "prompt": config["prompt"],
                "negative_prompt": config["negativePrompt"],
                "image": img_to_bytes(item[0]),
                "mask": img_to_bytes(item[1]),
                "num_outputs": appconfig.IMAGE_MODEL["numOutputs"],
                "num_inference_steps": int(config["inferenceSteps"]),
                "guidance_scale": float(config["guidanceScale"])
            }
        )
        output_urls.append(save_image_from_url(output[0]))

    output_image = reassemble_image(init_img, output_urls, inpaint_coords)
    local_img_url = save_image(output_image)

    if appconfig.DEBUG_MODE:
        save_image(mask_img, "mask_image.png", debug=True)
        save_image(init_img, "initial_image.png", debug=True)
        save_image(output_image, "inpainted_image.png", debug=True)
        for idx, (section_img, section_mask) in enumerate(inpaint_sections):
            save_image(section_img, str(idx) + "section_img.png", debug=True)
            save_image(section_mask, str(idx) + "section_mask.png", debug=True)

    return {"image_url": local_img_url}
