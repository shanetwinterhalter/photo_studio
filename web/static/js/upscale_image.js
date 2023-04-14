import { disableUi, updateImage } from "./ui.js";

export function upscaleImage() {
    disableUi(true);

    $.ajax({
        url: "/upscale_image",
        method: "POST",
        data: {
            image_url: $("#resultImage").attr("src")
        },
        success: function (response) {
            updateImage(response.image_url);
            disableUi(false);
        },
        error: function (error) {
            console.error(error);
            disableUi(false);
        }
    })
}