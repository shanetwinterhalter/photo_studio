// Prevent user sending multiple server requests
export function disableUi(enable) {
    if (enable) {
        $(".submitButton").prop("disabled", true);
        $("#loader").show();
    } else {
        $("#loader").hide();
        $(".submitButton").prop("disabled", false);
    }
}

export function updatePrompts() {
    $("#imgPrompt").val($("#imgPromptModal").val());
    $("#negativePrompt").val($("#negativePromptModal").val());
}

export function getZoomLevel() {
    const zoomContainer = $('#zoomContainer');
    return parseFloat(zoomContainer.css('transform').split(',')[3]) || 1;
}

// Toggle panning
export function toggleImagePanning(enable) {
    if (!!$("#zoomContainer").data("ui-draggable")) {
        if (enable) {
            $("#zoomContainer").draggable("enable");
        } else {
            $("#zoomContainer").draggable("disable");
        }
    }
}