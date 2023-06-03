from flask import (Flask, render_template, request,
                   jsonify, send_from_directory)
from src.generate import generate_image
from src.inpaint import inpaint_image
from src.segment import segment_image
from src.upload import upload_image
from src.utils.file_cleanup import cleanup_images
from threading import Thread

import src.appconfig as appconfig

app = Flask(__name__, static_url_path='/photo-studio/static')


@app.route('/', methods=['GET'])
def product_page():
    return render_template('main_page.html',
                           DEFAULTARGS=appconfig.DEFAULTARGS)


@app.route('/resources/<path:filename>')
def serve_resources(filename):
    return send_from_directory('resources', filename)


@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(appconfig.IMAGE_UPLOADS, filename)


@app.route('/call_model', methods=['POST'])
def call_model():
    action = request.form["action"]
    print(action)
    if action == "upload":
        response = upload_image(request.form)
    elif action == "generate":
        response = generate_image(request.form)
    elif action == "segment":
        response = segment_image(request.form)
    elif action == "inpaint":
        response = inpaint_image(request.form)
    else:
        response = ""
    return jsonify(response)


if __name__ == '__main__':
    file_deletion_thread = Thread(target=cleanup_images,
                                  daemon=True)
    file_deletion_thread.start()
    app.run(port=5001, debug=True)
