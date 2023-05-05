import { callModel } from './utils/serverRequest.js'
import { updateSegmentMask, loadMasksFromUrls } from './utils/maskUtils.js'
import { disableSegMaskUi } from './utils/uiUtils.js'

async function requestImageSegmentation() {
    // Set mask to null in case segmentation fails
    updateSegmentMask(null);

    // Disabled mask button
    disableSegMaskUi(true)

    callModel(
        "segment",
        async function (response) {
            try {
                const loadedMasks = await loadMasksFromUrls(response.image_mask);
                updateSegmentMask(loadedMasks);
            } catch (error) {
                console.error(`Error loading masks: ${error}`);
            } finally {
                disableSegMaskUi(false);
            }
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
