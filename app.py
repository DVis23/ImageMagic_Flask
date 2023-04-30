import base64
import io
from os.path import join

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
        return redirect(url_for('edit', filename=filename))
    return render_template('edit.html', photo=photo, filename=filename, filename_input=filename)


@app.route("/update_image", methods=["POST"])
def update_image():
    # Получаем значения ползунков и преобразуем их в числа
    filename = str(request.get_json()['filename'])

    bright_value = float(request.get_json()['brightness'])
    contrast_value = float(request.get_json()['contrast'])
    saturation_value = float(request.get_json()['saturation'])

    # Получаем изображение из POST-запроса
    img = Image.open(join('static', 'uploads', filename))
    # Обрабатываем изображение
    img = img.convert("RGB")
    if bright_value:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(float(bright_value))
    if contrast_value:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(float(contrast_value))
    if saturation_value:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(float(saturation_value))

    # Сохраняем измененное изображение в память
    image_buffer = io.BytesIO()
    img.save(image_buffer, format="JPEG")
    image_bytes = image_buffer.getvalue()
    # Возвращаем измененное изображение в формате base64-encoded JPEG
    return base64.b64encode(image_bytes).decode()


if __name__ == "__main__":
    app.run()