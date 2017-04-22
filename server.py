import os
from flask import Flask, request, render_template, send_from_directory
from werkzeug import secure_filename
from bson.json_util import loads
from time import time

# The root dir is the one where this python file is
UPLOAD_FOLDER = 'files'

# Allowed audio file extensions
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_valid_file(filename):
    if not '.' in filename:
        return False
    if not filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return False
    return True

@app.route("/css/<css_file>")
def css(css_file):
    css_url = 'css/' + css_file
    return render_template(css_url)
    
@app.route("/files/<img_file>")
def file_access(img_file):
    if os.path.isdir(app.config['UPLOAD_FOLDER']) == False:
        os.mkdir(app.config['UPLOAD_FOLDER'])

    return send_from_directory('files', img_file)

@app.route("/")
def index():
    return list_thumbnails()

@app.route("/upload", methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file_id = request.form['file_id']
        img_file = request.files['file']

        if img_file and is_valid_file(img_file.filename):
            # Generate a secure filename
            new_filename = (str(int(time() * 1000)) + ".png")
            safe_filename = secure_filename(new_filename)

            # Ensure that the upload folder exists
            if os.path.isdir(app.config['UPLOAD_FOLDER']) == False:
                os.mkdir(app.config['UPLOAD_FOLDER'])

            # Save our image file
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], safe_filename))

            return "File uploaded! id=" + file_id
        return "Failed!"

    # else:
    return render_template("upload.html")

@app.route("/list", methods=['GET'])
def list_thumbnails():
    if os.path.isdir(app.config['UPLOAD_FOLDER']) == False:
        os.mkdir(app.config['UPLOAD_FOLDER'])

    file_list = os.listdir('files/')
    file_list_str = ",".join(file_list)
    return file_list_str

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

