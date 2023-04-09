function convertFileToBase64(file, callback) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
        const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');
        callback(base64String);
    };
}

function updateImage(base64String) {
    image.src = `data:image/jpeg;base64,${base64String}`;
}

function generateImage(prompt) {
    const url = "/generate_image";

    const formData = new FormData();
    formData.append('prompt', prompt)

    fetch(url, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => updateImage(data.img_str))
        .catch(error => console.error('Error:', error));
}

function showLoadedImage() {
    const element = document.getElementById('loaded-image-div');
    element.style.display = 'block';
}

const generateButton = document.getElementById('generate-image-button');
const uploadFile = document.getElementById('file-upload');
const uploadButton = document.getElementById('upload-button');
const image = document.getElementById('loaded-image');

generateButton.addEventListener('click', () => {
    const prompt = document.getElementById('img-prompt').value;
    generateImage(prompt);
    showLoadedImage();
});

uploadButton.addEventListener('click', () => {
    const file = uploadFile.files[0];
    convertFileToBase64(file, (base64String) => {
        updateImage(base64String);
    });
    showLoadedImage();
})