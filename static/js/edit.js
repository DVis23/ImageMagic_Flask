function applyFilters() {
    const photo = document.getElementById('photo');
    const brightness = document.getElementById('brightness-slider').value;
    const contrast = document.getElementById('contrast-slider').value;
    const saturation = document.getElementById('saturation-slider').value;
    photo.style.filter = `brightness(${brightness}) contrast(${contrast}) saturate(${saturation})`;
}

document.querySelectorAll('input[type="range"]').forEach(el => {
    el.addEventListener('input', applyFilters);
});

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