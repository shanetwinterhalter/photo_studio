import requests

from .img_manip import remove_padding
from hashlib import md5
from PIL import Image
from io import BytesIO
from os import path

from .. import appconfig


def generate_filename(image):
    return f"{md5(image.tobytes()).hexdigest()}.png"


def save_image(image, filename=None, debug=False):
    if filename is None:
        filename = generate_filename(image)

    if debug:
        folder = appconfig.DEBUG_IMAGE_UPLOADS
    else:
        folder = appconfig.IMAGE_UPLOADS

    image_url = path.join(folder, filename)
    image.save(
        image_url,
        'PNG',
        quality=90
    )
    return image_url


def save_image_from_url(url, filename=None, debug=False, padding=(0, 0, 0, 0)):
    # Download image and save locally
    response = requests.get(url)
    response.raise_for_status()

    # Open the image using PIL
    image = Image.open(BytesIO(response.content))

    # Remove padding if needed
    if padding != (0, 0, 0, 0):
        image = remove_padding(image, padding)

    return save_image(image, filename, debug)


def img_to_bytes(img):
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes
