from src.actions import generate_image, segment_image, upload_image
from src.actions import upscale_image, inpaint_image
from flask import Flask, render_template, request, jsonify, send_from_directory
from src.image_fns import save_image
from PIL import Image
from src.utils import delete_old_files
from threading import Thread
from time import sleep

import src.appconfig as appconfig

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main_page.html',
                           DEFAULTARGS=appconfig.DEFAULTARGS)


@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(appconfig.IMAGE_UPLOADS, filename)


@app.route('/call_model', methods=['POST'])
def call_model():
    action = request.form["action"]
    print(action)
    for retry_count in range(appconfig.MAX_REQUEST_RETRIES):
        try:
            if action == "upload":
                response = upload_image(request.form)
            elif action == "generate":
                response = generate_image(request.form)
            elif action == "segment":
                response = segment_image(request.form)
            elif action == "upscale":
                response = upscale_image(request.form)
            elif action == "inpaint":
                response = inpaint_image(request.form)
            return jsonify(response)
        except RuntimeError:
            print(retry_count)
            print("CUDA out-of-memory when calling {}".format(action))
            if (retry_count < appconfig.MAX_REQUEST_RETRIES - 1) and (action != "segment"):
                sleep(appconfig.RETRY_DELAY)
            else:
                return "CUDA out-of-memory error: Please try again later.", 503


if __name__ == '__main__':
    file_deletion_thread = Thread(target=delete_old_files,
                                  daemon=True)
    file_deletion_thread.start()
    app.run(debug=True)
