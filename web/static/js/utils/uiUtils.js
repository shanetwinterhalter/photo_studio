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

export function getActiveEditButton() {
    const activeButton = $('input[name="imageEditRadio"]:checked').attr('id');
    toggleImagePanning(false)
    if (activeButton === "brushIcon") {
        return "brush";
    } else if (activeButton === "maskIcon") {
        return "segment";
    } else {
        toggleImagePanning(true)
        return "drag";
    }
}

export function resizeCanvas() {
    const canvas = $("#canvas")[0];
    const ctx = canvas.getContext("2d");
    const img = $("#resultImage")[0];

    const imageRect = img.getBoundingClientRect();
    const imageWidth = imageRect.width;
    const imageHeight = imageRect.height;

    // Create a temporary canvas and copy the current canvas content
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext("2d");
    tempCtx.drawImage(canvas, 0, 0);

    // Resize the main canvas
    canvas.width = imageWidth;
    canvas.height = imageHeight;

    // Redraw the content from the temporary canvas, scaling it to the new size
    ctx.drawImage(tempCanvas, 0, 0, tempCanvas.width, tempCanvas.height, 0, 0, canvas.width, canvas.height);
}


export function resizeAndRecentreImage() {
    const img = $("#resultImage");
    const zoomContainer = $("#zoomContainer");
    let optionsWidth = 0;
    let sidebarWidth = $("#optionGroups").width();
    if (!$("#userOptions").is(":hidden")) {
        optionsWidth = $("#userOptions").width();
    }
    const desiredWidth = window.innerWidth - sidebarWidth;
    const desiredHeight = window.innerHeight;

    const imgWidth = img.width();
    const imgHeight = img.height();
    const scaleX = desiredWidth / imgWidth;
    const scaleY = desiredHeight / imgHeight;
    const scale = Math.min(scaleX, scaleY);

    const leftPos = (window.innerWidth + optionsWidth - imgWidth * scale) / 2

    zoomContainer.css({
        left: leftPos,
        top: 0,
    });
}

export function disableSegMaskUi(loading) {
    if (loading) {
        console.log("Segmentation in progress, disabling UI")
        // Disable mask button and add loading icon
        $("#maskIcon").prop("disabled", true);
    } else {
        console.log("Segmentation complete, re-enabling UI")
        // Re-enable mask button and remove loading icon
        $("#maskIcon").prop("disabled", false);
    }
}
