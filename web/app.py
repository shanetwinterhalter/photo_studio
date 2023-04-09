from diffusers import StableDiffusionPipeline
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from torch import float16
from io import BytesIO
import base64

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_MODEL = "../models/shane9r"
NEGATIVE_PROMPT = "bad, deformed, ugly, bad anatomy, cartoon, animated," + \
                "scary, wrinkles, duplicate, double"
NUM_INFERENCE_STEPS = 15
GUIDANCE_SCALE = 20
INFERENCE_PIPE = StableDiffusionPipeline.from_pretrained(
            IMAGE_MODEL, torch_dtype=float16).to("cuda")

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
              filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_image(prompt):
    image = INFERENCE_PIPE(
        prompt,
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=NUM_INFERENCE_STEPS,
        guidance_scale=GUIDANCE_SCALE
        ).images[0]

    with BytesIO() as buffer:
        image.save(buffer, "JPEG")
        img_bytes = buffer.getvalue()

    return base64.b64encode(img_bytes).decode("utf-8")


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main_page.html')


@app.route('/generate_image', methods=['POST'])
def generate_image_request():
    print(request.form)
    prompt = request.form['prompt']
    print(prompt)
    image_str = generate_image(prompt)
    return {
        "img_str": image_str
    }


if __name__ == '__main__':
    app.run(debug=True)
