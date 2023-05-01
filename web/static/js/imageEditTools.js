import { getActiveEditButton, getZoomLevel, resizeCanvas } from './utils/uiUtils.js'
import { eventBus } from './utils/maskUtils.js'

let painting = false;
let toolMode;

const brushCap = "round";
const maskColor = "rgba(255, 255, 255, 0.75)";

const canvas = $("#canvas")[0];
const ctx = canvas.getContext("2d");
const img = $("#resultImage")[0];

let segmentationMasks;
let previousMask = null;
let currentSegmentIndex = 0;

eventBus.addEventListener("masksDataReceived", function (event) {
    segmentationMasks = event.detail;
});

function startPosition(e, toolMode) {
    painting = true;
    if (toolMode === "brush") {
        draw(e);
    } else if (toolMode === "segment") {
        //currentSegmentIndex = 0;
        applyPredefinedMask(e)
    }
}

function finishedPosition(toolMode) {
    painting = false;
    if (toolMode != "brush") return;
    ctx.beginPath();
}

function draw(e) {
    if (!painting) return;
    if (toolMode != "brush") return;

    const brushSize = $("#brushSizeSlider").val();

    const canvasRect = canvas.getBoundingClientRect();
    const zoomLevel = getZoomLevel()
    const x = (e.clientX - canvasRect.left) / zoomLevel;
    const y = (e.clientY - canvasRect.top) / zoomLevel;

    ctx.lineWidth = brushSize;
    ctx.lineCap = brushCap;
    ctx.strokeStyle = maskColor;

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

function applyMask(segmentMask, clear = false) {
    const zoomLevel = getZoomLevel();
    const scaleX = canvas.width / img.naturalWidth;
    const scaleY = canvas.height / img.naturalHeight;

    if (clear && previousMask) {
        for (let i = 0; i < previousMask.length; i++) {
            if (previousMask[i]) {
                const x = i % img.naturalWidth;
                const y = Math.floor(i / img.naturalWidth);
                ctx.clearRect(x * scaleX, y * scaleY, scaleX, scaleY);
            }
        }
    }

    for (let i = 0; i < segmentMask.length; i++) {
        if (segmentMask[i]) {
            const x = i % img.naturalWidth;
            const y = Math.floor(i / img.naturalWidth);
            ctx.fillStyle = maskColor;
            ctx.fillRect(x * scaleX, y * scaleY, scaleX, scaleY);
        }
    }

    previousMask = segmentMask;
}

function applyPredefinedMask(e) {
    console.log(currentSegmentIndex)
    if (toolMode != "segment") return;
    if (!segmentationMasks || !segmentationMasks.length) return;
    const canvasRect = canvas.getBoundingClientRect();
    const zoomLevel = getZoomLevel()
    const x = Math.floor((e.clientX - canvasRect.left) / zoomLevel);
    const y = Math.floor((e.clientY - canvasRect.top) / zoomLevel);

    const overlappingMasks = segmentationMasks.filter(maskData => {
        const row = maskData.segmentation[y];
        return row && row[x];
    });

    if (!overlappingMasks.length) return;

    overlappingMasks.sort((a, b) => a.area - b.area);

    const maskData = overlappingMasks[currentSegmentIndex % overlappingMasks.length].segmentation;
    const mask = [].concat(...maskData); // Flatten the 2D array
    const clearPreviousMask = currentSegmentIndex > 0;
    applyMask(mask, clearPreviousMask);
    currentSegmentIndex++;
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function configureCanvas() {
    img.addEventListener("load", function () {
        resizeCanvas();

        canvas.addEventListener("mousedown", function (e) {
            toolMode = getActiveEditButton();
            startPosition(e, toolMode);
        });
        canvas.addEventListener("mouseup", function () {
            toolMode = getActiveEditButton();
            finishedPosition(toolMode);
        });
        canvas.addEventListener("mousemove", function (e) {
            draw(e);
        });
    })
}

export function configureImageEditTools() {
    // Configure canvas whenever image is updated
    const observer = new MutationObserver((mutationsList, observer) => {
        // check if the src attribute has changed
        for (let mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'src') {
                clearCanvas();
                configureCanvas();
                break;
            }
        }
    });

    // configure the observer to watch for changes to the src attribute
    observer.observe($("#resultImage").get(0), { attributes: true, attributeFilter: ['src'] });
}
