import { disableUi, updateImage } from "./ui.js";
import { brushMask, segmentMask } from './createMask.js'

function maskToBase64(mask) {
    const uint8Array = new Uint8Array(mask.length);
    for (let i = 0; i < mask.length; i++) {
        uint8Array[i] = mask[i] ? 1 : 0;
    }
    
    let binaryString = '';
    const chunkSize = 8192;

    for (let i = 0; i < uint8Array.length; i += chunkSize) {
        const chunk = uint8Array.slice(i, i + chunkSize);
        binaryString += String.fromCharCode.apply(null, chunk);
    }
    return btoa(binaryString);
}

function combineMasks(brushMask, segmentMask) {
    if (brushMask.length != segmentMask.length) {
        throw "Mask sizes do not match";
    }

    const result = [];
    for (let i = 0; i < brushMask.length; i++) {
        result[i] = brushMask[i] || segmentMask[i];
    }

    return result
}

export function upscaleImage() {
    if($("#resultImage").attr("src") == null) {
        alert("Please upload an image first!");
        return;
    }
    disableUi(true);

    $.ajax({
        url: "/call_model",
        method: "POST",
        data: {
            action: "upscale",
            prompt: $("#imgPrompt").val(),
            image_url: $("#resultImage").attr("src"),
            negativePrompt: $("#negativePrompt").val(),
            inferenceSteps: $("#stepsSlider").val(),
            guidanceScale: $("#guidanceSlider").val(),
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

export function inpaintImage() {
    if($("#resultImage").attr("src") == null) {
        alert("Please upload an image first!");
        return;
    }
    disableUi(true);

    const mask = combineMasks(brushMask, segmentMask)
    const maskBase64 = maskToBase64(mask);

    $.ajax({
        url: "/call_model",
        method: "POST",
        data: {
            action: "inpaint",
            prompt: $("#imgPrompt").val(),
            image_url: $("#resultImage").attr("src"),
            mask: maskBase64,
            negativePrompt: $("#negativePrompt").val(),
            inferenceSteps: $("#stepsSlider").val(),
            guidanceScale: $("#guidanceSlider").val(),
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