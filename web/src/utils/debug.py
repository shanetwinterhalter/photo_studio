from PIL import Image, ImageDraw


def create_composite_image(image, mask, bounding_boxes=None,
                           section_boxes=None, grid_lines=False,
                           grid_size=512):
    # Create an image to draw the bounding boxes and mask on
    composite_img = image.copy()

    # Calculate the center of the image
    center_x = image.size[0] / 2
    center_y = image.size[1] / 2

    # Overlay mask on the image
    composite_img = Image.blend(composite_img, mask, alpha=0.5)
    draw = ImageDraw.Draw(composite_img)
    draw.point((center_x, center_y))

    # Draw each bounding box on the image
    if bounding_boxes is not None:
        for bbox in bounding_boxes:
            minr, minc, maxr, maxc = bbox
            draw.rectangle([minc, minr, maxc, maxr], outline="red", width=2)

    if section_boxes is not None:
        for section in section_boxes:
            minr, minc, maxr, maxc = section
            draw.rectangle([minc, minr, maxc, maxr], outline="blue", width=2)

        # Draw grid lines
    if grid_lines:
        for i in range(0, image.width, grid_size):
            draw.line([(i, 0), (i, image.height)], fill="blue", width=1)
        for i in range(0, image.height, grid_size):
            draw.line([(0, i), (image.width, i)], fill="blue", width=1)

    return composite_img
