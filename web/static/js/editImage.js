export function getActiveEditButton() {
    const activeButton = $(".edit-type:checked");
    enablePanning(false)
    if (activeButton.attr("id") === "brushIcon") {
        return "brush";
    } else if (activeButton.attr("id") === "maskIcon") {
        return "segment";
    } else {
        enablePanning(true)
        return "drag";
    }
}

// Toggle panning
function enablePanning(enable) {
    if (enable) {
        $("#zoomContainer").draggable("enable");
    } else {
        $("#zoomContainer").draggable("disable");
    }
}

// Initialize panning
export function initPanning() {
    $("#zoomContainer").draggable({
        cursor: "move",
        start: function (event, ui) {
            $(this).css("cursor", "grabbing");
        },
        stop: function (event, ui) {
            $(this).css("cursor", "grab");
        }
    });
}