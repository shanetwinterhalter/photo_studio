from .. import appconfig
from PIL import Image, ImageOps


def rotate_image(image):
    return ImageOps.exif_transpose(image)


def resize_image(image):
    width, height = image.size
    max_res = appconfig.MAX_IMAGE_RES

    if width > max_res[0] or height > max_res[1]:
        image.thumbnail(max_res, resample=Image.LANCZOS)

    return image


def make_square(image, padding_color=(0, 0, 0)):
    width, height = image.size
    max_dim = max(width, height)

    left_padding = (max_dim - width) // 2
    right_padding = max_dim - width - left_padding
    top_padding = (max_dim - height) // 2
    bottom_padding = max_dim - height - top_padding

    padding = (left_padding, top_padding, right_padding, bottom_padding)
    return (ImageOps.expand(image, padding, fill=padding_color), padding)


def remove_padding(image, padding=(0, 0, 0, 0)):
    left_padding, top_padding, right_padding, bottom_padding = padding
    width, height = image.size

    left = left_padding
    upper = top_padding
    right = width - right_padding
    lower = height - bottom_padding
    return image.crop((left, upper, right, lower))
