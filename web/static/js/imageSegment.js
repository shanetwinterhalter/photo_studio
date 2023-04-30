import { callModel } from './utils/serverRequest.js'
import { updateSegmentMask } from './utils/maskUtils.js'

function requestImageSegmentation() {
    // Set mask to null in case segmentation fails
    updateSegmentMask(null);

    callModel(
        "segment",
        function (response) {
            updateSegmentMask(response.image_mask);
        },
    );
}

export function configureImageSegmentation() {
    // create a new MutationObserver instance
    const observer = new MutationObserver((mutationsList, observer) => {
        // check if the src attribute has changed
        for (let mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'src') {
                requestImageSegmentation();
                break;
            }
        }
    });

    // configure the observer to watch for changes to the src attribute
    observer.observe($("#resultImage").get(0), { attributes: true, attributeFilter: ['src'] });
}
