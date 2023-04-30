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
        transform: `scale(${scale})`,
        left: leftPos,
        top: 0,
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
