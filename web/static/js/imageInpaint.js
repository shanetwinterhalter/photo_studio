import { callModel } from './utils/serverRequest.js'
import { updateImage } from './updateImage.js'
import { getCanvasBase64 } from './utils/convertToB64.js';

export function configureImageInpainting() {
    // When upscale button pressed
    $("#inpaintButton").on("click", function () {
        callModel(
            "inpaint",
            function (response) {
                updateImage(response.image_url);
            },
            null,
            getCanvasBase64(),
            );
    });
}