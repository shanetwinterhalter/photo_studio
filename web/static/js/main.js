import { uploadImage, generateImage, generateSegmentMask } from './loadImage.js';
import { configureSaveButton } from './imageDownload.js';
import { inpaintImage, upscaleImage } from './editImage.js';
import { configureCanvas } from './createMask.js';

// When upload button pressed
$("#uploadImageForm").on("submit", function (event) {
    event.preventDefault();
    uploadImage();
});

// When image generated
$("#generateImageForm").on("submit", function (event) {
    event.preventDefault();
    generateImage();
});

// Listener to request segment mask whenever image updated
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === "attributes" && mutation.attributeName === "src") {
            generateSegmentMask();
            configureCanvas();
        }
    });
});

observer.observe($("#resultImage")[0], {
    attributes: true,
    attributeFilter: ['src'],
})

// Request server to update image
$("#inpaintButton").on("click", function() {
    inpaintImage();
});
// Upscale image
$("#upscaleImageButton").on("click", function() {
    upscaleImage();
});

// On image saving
$("#saveImageButton").on("click", function() {
    configureSaveButton();
});

// Make edit icons exclusive
$(".icon-button").on("click", function () {
    $(".icon-button").removeClass("active");
    $(this).addClass("active");
});