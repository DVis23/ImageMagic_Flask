const fileInput = document.querySelector('input[type="file"]');
const fileName = document.querySelector('#file-name');

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        fileName.textContent = file.name;
    } else {
        fileName.textContent = 'No file chosen';
    }
});