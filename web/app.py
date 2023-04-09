from flask import Flask, render_template, request, redirect, url_for
import os

UPLOAD_FOLDER = "test_images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
              filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload():
    return render_template('main_page.html')


@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        return redirect(url_for('uploaded_file'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return "Uploaded file: {}".format(filename)


if __name__ == '__main__':
    app.run(debug=True)
