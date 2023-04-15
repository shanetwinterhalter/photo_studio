import { uploadImage } from './upload_image.js';
import { generateImage } from './generate_image.js';
import { inpaintImage } from './inpaint_image.js';
import { upscaleImage } from './upscale_image.js';
import { resizeImage } from './ui.js';
import { configureCanvas } from './drawing.js';
import { generateSegmentMask } from './image_segmentation.js';
import { configureSaveButton } from './image_download.js';

function onGenerateSubmit(event) {
    event.preventDefault();
    generateImage();
}

function onUploadSubmit(event) {
    event.preventDefault();
    uploadImage();
}

function imageSrcUpdate() {
    configureSaveButton();
    configureCanvas();
    generateSegmentMask();
}

$("#generateImageForm").submit(onGenerateSubmit);
$("#uploadImageForm").submit(onUploadSubmit);
$("#inpaintButton").click(inpaintImage);
$("#upscaleImageButton").click(upscaleImage);

// Run on any change to the image src
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === "attributes" && mutation.attributeName === "src") {
            imageSrcUpdate();
        }
    });
});

observer.observe($("#resultImage")[0], {
    attributes: true,
    attributeFilter: ['src'],
})

$(".icon-button").on("click", function () {
    $(".icon-button").removeClass("active");

    $(this).addClass("active");
});

window.addEventListener("resize", resizeImage);
