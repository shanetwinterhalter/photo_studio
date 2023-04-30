import { callModel } from './utils/serverRequest.js'
import { getImageBase64 } from './utils/convertToB64.js'
import { updateImage } from './updateImage.js'

export async function configureImageUpload() {
    // When upload button pressed
    $("#uploadImageForm").on("submit", function (event) {
        event.preventDefault();
        const promise = getImageBase64();

        promise.then(function (imageBase64) {
            callModel(
                "upload",
                function (response) {
                    updateImage(response.image_url);
                },
                imageBase64
            );
        }).catch(function (error) {
            alert(error);
        });
    });
}
