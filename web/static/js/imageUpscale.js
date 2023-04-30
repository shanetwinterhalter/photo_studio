import { callModel } from './utils/serverRequest.js'
import { updateImage } from './updateImage.js'

export function configureImageUpscaling() {
    // When upscale button pressed
    $("#upscaleImageButton").on("click", function () {
        callModel(
            "upscale",
            function (response) {
                updateImage(response.image_url);
            });
    });
}
