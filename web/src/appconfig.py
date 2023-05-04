DEFAULTARGS = {
    "prompt": "a portrait photo of a shane man, handsome, " +
              "clear skin, ",
    "inferenceSteps": "30",
    "guidanceScale": "8",
    "negativePrompt": "bad, deformed, ugly, bad anatomy, cartoon, " +
                      "animated, scary, wrinkles, duplicate, double",
    "brushSize": "10",
    "systemPrompt": "photograph, photorealistic, well lit, beautiful, " +
                    "ultra realistic, hyper detail, unedited, symmetrical " +
                    "balance, in-frame",
    "negativeSystemPrompt": "((out of frame)), ((extra fingers)), mutated "
                            "hands, ((poorly drawn hands)), ((poorly drawn "
                            "face)), (((mutation))), (((deformed))), " +
                            "(((tiling))), ((naked)), ((tile)), " +
                            "((fleshpile)), ((ugly)), (((abstract))), " +
                            "blurry, ((bad anatomy)), ((bad proportions)), " +
                            "((extra limbs)), cloned face, (((skinny))), " +
                            "glitchy, ((extra breasts)), ((double torso)), " +
                            "((extra arms)), ((extra hands)), ((mangled " +
                            "fingers)), ((missing breasts)), (missing lips)," +
                            " ((ugly face)), ((fat)), ((extra legs)), anime"
}

IMAGE_MODEL = {
    "modelName": "stability-ai/stable-diffusion",
    "modelVersion": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
    "numOutputs": 1,
    "dimensions": "768x768",
    "scheduler": "DPMSolverMultistep"
}

SEGMENT_MODEL = "../models/sam_vit_h_4b8939.pth"
MAX_SEGMENT_RES = (1920, 1920)

UPSCALE_MODEL = "stabilityai/stable-diffusion-x4-upscaler"
UPSCALE_RES = (256, 256)

INPAINT_MODEL = "stabilityai/stable-diffusion-2-inpainting"
MAX_INPAINT_RES = (1024, 1024)

MAX_REQUEST_RETRIES = 6
RETRY_DELAY = 20

DEBUG_IMAGE_UPLOADS = 'debug_images'
IMAGE_UPLOADS = 'images'
MAX_IMAGE_AGE_HOURS = 24
