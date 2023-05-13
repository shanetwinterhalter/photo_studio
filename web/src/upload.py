from PIL import Image
from base64 import b64decode
from io import BytesIO
from .utils.img_manip import rotate_image, resize_image
from .utils.img_ops import save_image


def upload_image(config):
    image_data = BytesIO(b64decode(config["image"].split(",")[1]))
    image = Image.open(image_data).convert('RGB')

    # Rotate images if needed
    image = rotate_image(image)

    # Resize image to max size if larger
    image = resize_image(image)

    return {"image_url": save_image(image)}
