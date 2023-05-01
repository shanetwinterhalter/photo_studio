import { resizeAndRecentreImage } from "./utils/uiUtils.js";

function configureImageZoom() {
    // Bind the mousewheel event to the zoomContainer
    $('#zoomContainer').on('wheel', function (e) {
        e.preventDefault();

        // Calculate the zoom factor
        const delta = e.originalEvent.deltaY < 0 ? 1.05 : 0.95;
        const currentScale = parseFloat($(this).css('transform').split(',')[3]) || 1;
        const newScale = currentScale * delta;

        // Apply the new scale
        $(this).css('transform', `scale(${newScale})`);
    });
}

// Initialize panning
function configureImagePanning() {
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

export function updateImage(imageUrl) {
    const img = $("#resultImage")
    img.attr("src", imageUrl);
    img.show();
    img.one("load", function () {
        resizeAndRecentreImage();
        configureImageZoom();
        configureImagePanning();
    });
}
