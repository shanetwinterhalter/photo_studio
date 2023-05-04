from src.actions import (generate_image, segment_image,
                         upload_image, inpaint_image)
from flask import (Flask, render_template, request,
                   jsonify, send_from_directory)
from src.utils import cleanup_images
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
    if action == "upload":
        response = upload_image(request.form)
    elif action == "generate":
        response = generate_image(request.form)
    elif action == "segment":
        response = segment_image(request.form)
    elif action == "inpaint":
        response = inpaint_image(request.form)
    return jsonify(response)


if __name__ == '__main__':
    file_deletion_thread = Thread(target=cleanup_images,
                                  daemon=True)
    file_deletion_thread.start()
    app.run(debug=True)
