import { getMask } from './mask.js'
import { eventBus } from './eventBus.js'

// Prevent user sending multiple server requests
function disableUi(enable) {
    if (enable) {
        $("#loadedImageDisplay").show();
        $(".submitButton").prop("disabled", true);
        $("#loader").show();
    } else {
        $("#loader").hide();
        $(".submitButton").prop("disabled", false);
    }
}

function getImageMaskBase64() {
    const mask = getMask();
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

function getImageBase64() {
    return new Promise((resolve, reject) => {
        const fileInput = document.getElementById("fileUpload");
        const file = fileInput.files[0];

        if (!file) {
            alert("Please select a file to upload");
            return;
        }

        const reader = new FileReader();
        reader.onloadend = function () {
            const base64data = reader.result;
            resolve(base64data);
        }
        reader.onerror = function () {
            reject("Error reading file");
        }
        reader.readAsDataURL(file);
    });
}

function updateImage(imageUrl) {
    const img = $("#resultImage")
    img.attr("src", imageUrl);
    img.show();
}

export async function callModel(action) {
    if (action != "segment") { disableUi(true); }
    let maskBase64 = null;
    let imageBase64 = null;

    if (action == "inpaint") {
        maskBase64 = getImageMaskBase64();
    }

    if (action == "upload") {
        try {
            imageBase64 = await getImageBase64();
        } catch (error) {
            alert(error);
            disableUi(false);
            return;
        }
    }

    $.ajax({
        url: "/call_model",
        method: "POST",
        data: {
            action: action,
            prompt: $("#imgPrompt").val(),
            image_url: $("#resultImage").attr("src"),
            mask: maskBase64,
            image: imageBase64,
            negativePrompt: $("#negativePrompt").val(),
            inferenceSteps: $("#stepsSlider").val(),
            guidanceScale: $("#guidanceSlider").val(),
        },
        success: function (response) {
            if (action == "segment") {
                eventBus.dispatchEvent(new CustomEvent("masksDataReceived", { detail: response.image_mask }));
            } else {
                updateImage(response.image_url);
                disableUi(false);
            }
        },
        error: function (error) {
            console.error(error);
            disableUi(false);            
        }
    })
}
