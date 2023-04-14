import { disableUi, updateImage } from './ui.js';
import { mask } from './drawing.js'

function maskToBinaryString(mask) {
    let binaryString = "";
    for (let i = 0; i < mask.length; i += 8) {
        let byte = 0;
        for (let j = 0; j < 8; j++) {
            byte |= (mask[i + j] << j);
        }
        binaryString += String.fromCharCode(byte);
    }
    return binaryString;
}

function binaryStringToBase64(binaryString) {
    return btoa(unescape(encodeURIComponent(JSON.stringify(mask))));
}

export function inpaintImage() {
    disableUi(true);

    const maskBinaryString = maskToBinaryString(mask);
    const maskBase64 = binaryStringToBase64(maskBinaryString);

    $.ajax({
        url: "/inpaint_image",
        method: "POST",
        data: {
            image_url: $("#resultImage").attr("src"),
            mask: maskBase64
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