import numpy as np
import requests

from . import appconfig
from base64 import b64decode
from hashlib import md5
from io import BytesIO
from os import path
from PIL import Image, ImageOps


def rotate_image(image):
    return ImageOps.exif_transpose(image)


def save_image(image, filename=None, debug=False):
    if filename is None:
        filename = f"{md5(image.tobytes()).hexdigest()}.png"

    if debug:
        folder = appconfig.DEBUG_IMAGE_UPLOADS
    else:
        folder = appconfig.IMAGE_UPLOADS

    image.save(
        path.join(folder, filename),
        'PNG',
        quality=90
    )
    image_url = f"{folder}/{filename}"
    return image_url


def save_image_from_url(url, filename=None, debug=False, padding=(0, 0, 0, 0)):
    if debug:
        folder = appconfig.DEBUG_IMAGE_UPLOADS
    else:
        folder = appconfig.IMAGE_UPLOADS

    # Download image and save locally
    response = requests.get(url)
    response.raise_for_status()

    # Open the image using PIL
    image = Image.open(BytesIO(response.content))

    # Remove padding if needed
    if padding != (0, 0, 0, 0):
        image = remove_padding(image, padding)

    # Generate filename from image hash
    if filename is None:
        filename = f"{md5(image.tobytes()).hexdigest()}.png"

    image_url = path.join(folder, filename)
    image.save(image_url)

    return image_url


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
    print(f"Adding padding: {padding}")
    return (ImageOps.expand(image, padding, fill=padding_color), padding)


def remove_padding(image, padding=(0, 0, 0, 0)):
    print(f"Removing padding: {padding}")
    left_padding, top_padding, right_padding, bottom_padding = padding
    width, height = image.size

    left = left_padding
    upper = top_padding
    right = width - right_padding
    lower = height - bottom_padding
    print(f"Calculated crop values: {(left, upper, right, lower)}")
    return image.crop((left, upper, right, lower))


def create_mask_image(b64_mask_string, size):
    decoded_mask = b64decode(b64_mask_string)
    height, width = size

    # Decode mask and create NumPy array
    mask_array = np.frombuffer(
        decoded_mask,
        dtype=np.uint8
        ).reshape(width, height) * 255

    # Create mask image and resize
    mask_img = Image.fromarray(mask_array).convert("RGB")
    mask_img = mask_img.resize(size)

    return mask_img


def img_to_bytes(img):
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes
