import { getActiveEditButton, resizeCanvas, fillTempCanvas } from './utils/uiUtils.js'
import { eventBus } from './utils/maskUtils.js'

let painting = false;
let toolMode;

const brushCap = "round";
const maskColor = "rgba(255, 255, 255, 0.75)";

const canvas = $("#canvas")[0];
const ctx = canvas.getContext("2d");
const img = $("#resultImage")[0];
const tempCanvas = $("#tempCanvas")[0];


let segmentationMasks;
let currentSegmentIndex = 0;

eventBus.addEventListener("masksDataReceived", function (event) {
    segmentationMasks = event.detail;
});

function startPosition(e, toolMode) {
    painting = true;
    if (toolMode === "brush") {
        draw(e);
    } else if (toolMode === "segment") {
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

    const x = e.offsetX;
    const y = e.offsetY;

    ctx.lineWidth = brushSize;
    ctx.lineCap = brushCap;
    ctx.strokeStyle = maskColor;

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

function applyPredefinedMask(e) {
    if (!segmentationMasks || !segmentationMasks.length) return;

    ctx.fillStyle = maskColor;

    const canvasRect = canvas.getBoundingClientRect();
    const x_click = e.offsetX;
    const y_click = e.offsetY;

    const overlappingMasks = segmentationMasks.filter(mask => {
        const maskX = x_click * mask.width / img.width;
        const maskY = y_click * mask.height / img.height;
        const pixelData = mask.getContext('2d').getImageData(maskX, maskY, 1, 1).data;
        return pixelData[3] > 0; // Check if the alpha channel value is greater than 0
    });

    if (overlappingMasks.length > 0) {
        const maskIndex = currentSegmentIndex % overlappingMasks.length;
        const mask = overlappingMasks[maskIndex];

        ctx.clearRect(0, 0, canvas.width, canvas.height)
        // Draw brush masks back on
        ctx.drawImage(tempCanvas, 0, 0);
        ctx.drawImage(mask, 0, 0, img.width, img.height);
        ctx.globalCompositeOperation = 'source-over';
    }

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

    // When mask button selected, copy to temp 
    $("#maskIcon").on("click", function (event) {
        fillTempCanvas();
    });
}
