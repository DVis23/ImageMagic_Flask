document.querySelectorAll('input[type="range"]').forEach(el => {
    el.addEventListener('input', updateImage);
});

function updateImage() {
    // Получаем значения ползунков
    const filename = document.getElementById("filename_input").value;

    const brightnessValue = document.getElementById("brightness-slider").value;
    const contrastValue = document.getElementById("contrast-slider").value;
    const saturationValue = document.getElementById("saturation-slider").value;

    // Отправляем AJAX-запрос на серверную часть
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/update_image");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Обновляем изображение на странице
            document.getElementById("photo").src = "data:image/jpeg;base64," + xhr.responseText;
        } else {
            console.log("Error occurred while updating the image");
        }
    };
    xhr.send(JSON.stringify({
        filename: filename,
        brightness: brightnessValue,
        contrast: contrastValue,
        saturation: saturationValue
    }));
}

document.getElementById('download-btn').addEventListener('click', function() {

    // Создаем временный canvas
    var photo = document.getElementById('photo');
    var canvas = document.createElement('canvas');
    canvas.width = photo.naturalWidth; // использовать naturalWidth и naturalHeight для сохранения размеров оригинального изображения
    canvas.height = photo.naturalHeight;
    var context = canvas.getContext('2d');

    var brightness = document.getElementById('brightness-slider').value;
    var contrast = document.getElementById('contrast-slider').value;
    var saturation = document.getElementById('saturation-slider').value;
    context.filter = `brightness(${brightness}) contrast(${contrast}) saturate(${saturation})`;

    // Загружаем оригинальное изображение в объект Image
    var img = new Image();
    img.onload = function() {
        // Рисуем оригинальное изображение на canvas
        context.drawImage(img, 0, 0, canvas.width, canvas.height);

        // Создаем ссылку для скачивания файла
        var downloadLink = document.createElement('a');
        downloadLink.setAttribute('download', 'edited_photo.jpg'); // имя файла для скачивания
        downloadLink.setAttribute('href', canvas.toDataURL()); // ссылка на отредактированное изображение
        downloadLink.click(); // скачиваем файл
    };
    img.src = photo.src;
});