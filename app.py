from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_uploads import UploadSet, IMAGES, configure_uploads
from PIL import ImageEnhance, Image


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
app.config['UPLOADED_PHOTOS_ALLOW'] = set(['png', 'jpg', 'jpeg'])
configure_uploads(app, photos)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return redirect(url_for('edit', filename=filename))
    return render_template('index.html')


@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit(filename):
    photo = photos.url(filename)
    if request.method == 'POST':
        img = Image.open(photos.path(filename))
        bright_value = request.form.get('brightness')
        contrast_value = request.form.get('contrast')
        saturation_value = request.form.get('saturation')
        if bright_value:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(float(bright_value))
        if contrast_value:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(float(contrast_value))
        if saturation_value:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(float(saturation_value))
        img.save(photos.path(filename))
        return redirect(url_for('download', filename=filename))
    return render_template('edit.html', photo=photo)


@app.route('/download/<filename>')
def download(filename):
    path = photos.path(filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run()
