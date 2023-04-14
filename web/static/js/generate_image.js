import { disableUi, updateImage } from './ui.js';

export function generateImage() {
    disableUi(true);

    $.ajax({
        url: "/generate_image",
        method: "POST",
        data: {
            prompt: $("#imgPrompt").val()
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