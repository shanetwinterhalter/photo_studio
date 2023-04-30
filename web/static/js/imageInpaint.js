import { callModel } from './utils/serverRequest.js'
import { updateImage } from './updateImage.js'
import { getMaskBase64 } from './utils/convertToB64.js';
import { mask } from './imageEditTools.js'

export function configureImageInpainting() {
    const maskBase64 = getMaskBase64(mask);

    // When upscale button pressed
    $("#inpaintButton").on("click", function () {
        callModel(
            "inpaint",
            function (response) {
                updateImage(response.image_url);
            },
            imageBase64 = null,
            maskBase64 = maskBase64,
            );
    });
}