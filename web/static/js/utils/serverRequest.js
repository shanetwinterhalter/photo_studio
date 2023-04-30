import { disableUi } from './uiUtils.js'

export async function callModel(
    action,
    successFunction,
    imageBase64 = null,
    maskBase64 = null
    ) {
        if (action != "segment") { disableUi(true); }

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
            success: successFunction,
            error: function (error) {
                console.error(error);
            },
            complete: function() {
                disableUi(false)
            }
        })
}
