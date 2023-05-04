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

    # Rotate images if needed
    image = rotate_image(image)

    image.save(
        path.join(folder, filename),
        'PNG',
        quality=90
    )
    image_url = f"{folder}/{filename}"
    return image_url


def save_image_from_url(url, filename=None, debug=False):
    if debug:
        folder = appconfig.DEBUG_IMAGE_UPLOADS
    else:
        folder = appconfig.IMAGE_UPLOADS

    # Download image and save locally
    response = requests.get(url)
    response.raise_for_status()

    # Open the image using PIL
    image = Image.open(BytesIO(response.content))

    # Generate filename from image hash
    if filename is None:
        filename = f"{md5(image.tobytes()).hexdigest()}.png"

    image_url = path.join(folder, filename)
    image.save(image_url)

    return image_url


def resize_image(image, max_res):
    width, height = image.size
    if width > max_res[0] or height > max_res[1]:
        if width > height:
            new_width = max_res[0]
            new_height = int(height * new_width / width)
        else:
            new_height = max_res[1]
            new_width = int(width * new_height / height)
        return image.resize((new_width, new_height))
    else:
        return image


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
