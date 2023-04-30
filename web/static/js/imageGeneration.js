import { updatePrompts } from './utils/uiUtils.js'
import { callModel } from './utils/serverRequest.js'
import { updateImage } from './updateImage.js'

export function configureImageGeneration() {
    // When upload button pressed
    $("#generateImageButton").on("click", function (event) {
        event.preventDefault();
        updatePrompts();

        callModel(
            "generate",
            function (response) {
                updateImage(response.image_url);
            });
    });
}
