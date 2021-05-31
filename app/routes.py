import os
from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import generator
from werkzeug.utils import secure_filename
from detection import detection


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    thr = request.form['thr']
    network = request.form.get('network')
    print(network)
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{generator.next()}.{get_extension(filename)}"#secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded')
        return render_template('upload.html', filename=filename, thr=thr, network=network)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)


@app.route('/output/<filename>')
def output_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='outputs/' + filename), code=301)


@app.route('/process', methods=['POST'])
def process():
    json = jsonify({'filename': transform(request.form['filename'], request.form['thr'], request.form.get('network'))})
    #clear(request.form['filename'])
    #flash('Image processed')
    return json


# def clear(filename):
#     print("remove files")
#     path = os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename)
#     outpath = os.path.join(app.config['OUTPUT_IMAGES_DEST'], get_output_filename(filename))
#     if os.path.exists(path):
#         os.remove(path)
#     if os.path.exists(outpath):
#         os.remove(outpath)


def transform(filename, thr, network):
    print("transform " + filename)
    print(network)
    # if os.path.isfile(os.path.join(app.config['UPLOADED_IMAGES_DEST'], f"out_{filename}")):
    #     print("dfd")
    img_path = f"{app.config['UPLOADED_IMAGES_DEST']}/{filename}"
    output_filename = get_output_filename(filename)
    out_path = f"{app.config['OUTPUT_IMAGES_DEST']}/{output_filename}"
    detection(img_path, out_path, thr, network)
    return output_filename


def get_output_filename(filename):
    image_name = filename.rsplit('.', 1)[0]
    return f'output_{image_name}.png'


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ""


def allowed_file(filename):
    return get_extension(filename) in app.config['ALLOWED_EXTENSIONS']