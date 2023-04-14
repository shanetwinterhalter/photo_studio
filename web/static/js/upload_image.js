import { disableUi, updateImage } from './ui.js';

export function uploadImage() {
    const fileInput = document.getElementById("fileUpload");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to upload");
        return;
    }
    disableUi(true);
    
    const formData = new FormData();
    formData.append("image", file);

    $.ajax({
        url: "/upload_image",
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            updateImage(data.image_url);
            disableUi(false);
        },
        error: function (jqXHR, textStatus, errorMessage) {
            console.error("Upload failed:", textStatus, errorMessage);
            disableUi(false);
        }
    })
}