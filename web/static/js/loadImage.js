import { disableUi, updateImage } from './ui.js';
import { eventBus } from "./eventBus.js";

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

export function generateImage() {
    disableUi(true);

    $.ajax({
        url: "/generate_image",
        method: "POST",
        data: {
            prompt: $("#imgPrompt").val(),
            negativePrompt: $("#negativePrompt").val(),
            inferenceSteps: $("#stepsSlider").val(),
            guidanceScale: $("#guidanceSlider").val(),
        },
        success: function (response) {
            updateImage(response.image_url);
            disableUi(false)
        },
        error: function (error) {
            console.error(error);
            disableUi(false)
        }
    })
}

export function generateSegmentMask() {    
    $.ajax({
        url: "/segment_image",
        method: "POST",
        data: {
            image_url: $("#resultImage").attr("src")
        },
        success: function (response) {
            eventBus.dispatchEvent(new CustomEvent("masksDataReceived", { detail: response.image_mask }));
            console.log("Image segmentation complete")
        },
        error: function (error) {
            console.log(error);
        }
    })
}