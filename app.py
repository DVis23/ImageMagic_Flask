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
    return render_template('edit.html', photo=photo, filename=filename)


if __name__ == "__main__":
    app.run()
