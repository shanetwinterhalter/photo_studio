DEBUG_MODE = False
DEBUG_IMAGE_UPLOADS = 'debug_images'

ENABLE_SEGMENTATION = False
MAX_IMAGE_RES = (1024, 1024)
IMAGE_UPLOADS = 'images'
MAX_IMAGE_AGE_HOURS = 24

DEFAULTARGS = {
    "prompt": "a portrait photo of a person",
    "inferenceSteps": "30",
    "guidanceScale": "8",
    "maxGuidanceScale": "20",
    "negativePrompt": "bad, deformed, ugly, bad anatomy, cartoon, " +
                      "animated, scary, wrinkles, duplicate, double",
    "brushSize": "20",
    "systemPrompt": "photograph, photorealistic, well lit, beautiful, " +
                    "ultra realistic, hyper detail, unedited, symmetrical " +
                    "balance, in-frame",
    "negativeSystemPrompt": "out of frame, extra fingers, mutated "
                            "hands, poorly drawn hands, poorly drawn "
                            "face, mutation, deformed, " +
                            "tiling, naked, tile, " +
                            "fleshpile, ugly, abstract, " +
                            "blurry, bad anatomy, bad proportions, " +
                            "extra limbs, cloned face, " +
                            "glitchy, extra breasts, double torso, " +
                            "extra arms, extra hands, mangled " +
                            "fingers, missing breasts, missing lips," +
                            " ugly face, extra legs"
}

IMAGE_MODEL = {
    "modelName": "stability-ai/stable-diffusion",
    "modelVersion": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
    "numOutputs": 1,
    "dimensions": "768x768",
    "scheduler": "DPMSolverMultistep"
}

INPAINT_MODEL = {
    "modelName": "stability-ai/stable-diffusion-inpainting",
    "modelVersion": "c28b92a7ecd66eee4aefcd8a94eb9e7f6c3805d5f06038165407fb5cb355ba67",
    "numOutputs": 1
}

SEGMENT_MODEL = {
    "modelName": "shanetwinterhalter/segment-anything-model",
    "modelVersion": "0c5dd33132c5e5863ed72223e9c9166f2dc81e6d98f10368c15c1db82b4102c1",
    "maxHeight": 1024,
    "maxWidth": 1024
}
