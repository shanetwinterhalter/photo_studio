import numpy as np

from base64 import b64decode
from PIL import Image


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
