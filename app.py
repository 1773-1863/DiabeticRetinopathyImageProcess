from flask import Flask, request, render_template, redirect, flash, url_for
import urllib.request
import os
import os.path
from werkzeug.utils import secure_filename
from converter import converter

UPLOAD_FOLDER = "static/uploaded_images"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('index_2.html')

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             reading_path = "static/uploaded_images/"  # IMPORTANT
#             saving_path = "static/processed_images/"  # IMPORTANT
#             a = converter(reading_path, filename, saving_path)
#             return redirect(url_for('upload_file', name=file.filename))
#     return render_template("index_2.html")
#
# @app.route('/show', methods=['GET'])
# def show():
#     hists = os.listdir('static/processed_images')
#     hists = ['processed_images/' + file for file in hists]
#     return render_template('show.html', hists=hists)

@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            reading_path = "static/uploaded_images/"  # IMPORTANT
            saving_path = "static/processed_images/"  # IMPORTANT
            converter(reading_path, filename, saving_path)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

    return render_template('index_2.html', filenames=file_names)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename="/" + filename), code=301)

@app.route('/show/<filename>')
def show(filename):
    return redirect(url_for('static', filename="/processed_images/"+filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
