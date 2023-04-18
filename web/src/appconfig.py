DEFAULTARGS = {
    "prompt": "a portrait photo of a shane man, handsome, " +
              "clear skin, photograph, photorealistic, well lit",
    "inferenceSteps": "15",
    "guidanceScale": "7.5",
    "negativePrompt": "bad, deformed, ugly, bad anatomy, cartoon, " +
                      "animated, scary, wrinkles, duplicate, double"
}

IMAGE_MODEL = "../models/shane9r"
SEGMENT_MODEL = "../models/sam_vit_h_4b8939.pth"

UPSCALE_MODEL = "stabilityai/stable-diffusion-x4-upscaler"
UPSCALE_RES = (256, 256)

INPAINT_MODEL = "stabilityai/stable-diffusion-2-inpainting"
MAX_INPAINT_RES = (1024, 1024)

MAX_REQUEST_RETRIES = 6
RETRY_DELAY = 20

IMAGE_UPLOADS = 'images'
MAX_IMAGE_AGE_HOURS = 24
