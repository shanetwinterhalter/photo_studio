import { initPanning } from './editImage.js'
import { configureCanvas } from './canvas.js'

function imageUpdateListener() {
    // Listener for changes to display Image
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === "attributes" && mutation.attributeName === "src") {
                // TODO: Re-enable segment masks
                generateSegmentMask();
                initPanning();
                configureCanvas();
            }
        });
    });
    observer.observe($("#resultImage")[0], {
        attributes: true,
        attributeFilter: ['src'],
    })
}

function imageZoomListener() {
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

export function configureContent() {
    imageUpdateListener();
    imageZoomListener();
}
