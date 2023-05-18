import { setupUi } from './uiSetup.js'
import { configureImageUpload } from './imageUpload.js'
import { configureImageGeneration } from './imageGeneration.js'
import { configureImageInpainting } from './imageInpaint.js'
import { configureImageSaving } from './imageSave.js'
import { configureImageEditTools } from './imageEditTools.js'
import { configureImageSegmentation } from './imageSegment.js'

import { resizeCanvas, resizeAndRecentreImage } from './utils/uiUtils.js'

$(document).ready(function () {
    // Initial UI setup
    setupUi();

    // Image upload
    configureImageUpload();

    // Image generation
    configureImageGeneration();

    // Image Inpaint
    configureImageInpainting();

    // Image Save
    configureImageSaving();

    // Open load image modal
    $("#imageModal").modal("show");

    // Configure image segmentation
    configureImageSegmentation();

    // Content
    configureImageEditTools();

    // Resize and reconfigure image when window resized
    window.addEventListener("resize", () => {
      $('#zoomContainer').css('transform', 'scale(1)');
      resizeAndRecentreImage();
      resizeCanvas();
    });
});