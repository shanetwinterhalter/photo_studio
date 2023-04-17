import { eventBus } from "./eventBus.js";

let brushMask;
let segmentMask;
let toolMode;
let painting = false;
const brushCap = "round";
const maskColor = "rgba(255, 255, 255, 0.75)";

let canvas;
let ctx;
let img;

let segmentationMasks;
let currentSegmentIndex = 0;
eventBus.addEventListener("masksDataReceived", function (event) {
    segmentationMasks = event.detail;
});

function getActiveEditButton() {
    const activeButton = $(".icon-button.active");
    if (activeButton.attr("id") === "brushIcon") {
        return "brush";
    } else if (activeButton.attr("id") === "maskIcon") {
        return "segment";
    } else {
        return null;
    }
}

function startPosition(e, toolMode) {
    painting = true;

    if (toolMode === "brush") {
        draw(e);
    } else if (toolMode === "segment") {
        currentSegmentIndex = 0;
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

    const canvasRect = $("#canvas")[0].getBoundingClientRect();
    const x = Math.floor(e.clientX - canvasRect.left);
    const y = Math.floor(e.clientY - canvasRect.top);
    let brushSize = $("#brushSizeSlider").val();

    ctx.lineWidth = brushSize;
    ctx.lineCap = brushCap;
    ctx.strokeStyle = maskColor;

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);

    for (let i = -brushSize; i < brushSize; i++) {
        for (let j = -brushSize; j < brushSize; j++) {
            if (i * i + j * j < brushSize * brushSize) {
                const index = (y + j) * img.naturalWidth + (x + i);
                if (index >= 0 && index < brushMask.length) {
                    brushMask[index] = 1;
                }
            }
        }
    }
}

function applyPredefinedMask(e) {
    if (!segmentationMasks || !segmentationMasks.length) return;
  
    const canvasRect = canvas.getBoundingClientRect();
    const x = Math.floor(e.clientX - canvasRect.left);
    const y = Math.floor(e.clientY - canvasRect.top);
  
    const overlappingMasks = segmentationMasks.filter(maskData => {
        const row = maskData.segmentation[y];
        return row && row[x];
    });

    if (!overlappingMasks.length) return;

    overlappingMasks.sort((a, b) => a.area - b.area);
  
    const maskData = overlappingMasks[currentSegmentIndex % overlappingMasks.length].segmentation;
    const mask = [].concat(...maskData); // Flatten the 2D array
  
    for (let i = 0; i < mask.length; i++) {
      if (mask[i] && !brushMask[i]) {
        segmentMask[i] = 1;
      }
    }

    // Clear the segmentMask array
    segmentMask.fill(0);

    for (let i = 0; i < mask.length; i++) {
        if (mask[i] && !brushMask[i]) {
          segmentMask[i] = 1;
        }
    }

    currentSegmentIndex++;
  
    // Redraw the canvas with the updated mask
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);

    for (let i = 0; i < segmentMask.length; i++) {
        if (segmentMask[i]) {
            const x = i % img.naturalWidth;
            const y = Math.floor(i / img.naturalWidth);
            ctx.fillStyle = maskColor;
            ctx.fillRect(x, y, 1, 1);
        }
    }

    // Draw brush strokes on top of the segment mask
    for (let i = 0; i < brushMask.length; i++) {
        if (brushMask[i]) {
            const x = (i % img.naturalWidth);
            const y = Math.floor(i / img.naturalWidth);
            ctx.fillStyle = maskColor;
            ctx.fillRect(x, y, 1, 1);
        }
    }
}

export function configureCanvas() {
    canvas = $("#canvas")[0];
    ctx = canvas.getContext("2d");
    img = $("#resultImage")[0];

    img.addEventListener("load", function () {
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        brushMask = new Array(img.naturalWidth * img.naturalHeight).fill(0);
        segmentMask = new Array(img.naturalWidth * img.naturalHeight).fill(0);

        canvas.addEventListener("mousedown", function(e) {
            toolMode = getActiveEditButton();
            startPosition(e, toolMode);
        });
        canvas.addEventListener("mouseup", function() {
            toolMode = getActiveEditButton();
            finishedPosition(toolMode);
        });
        canvas.addEventListener("mousemove", function (e) {
            toolMode = getActiveEditButton();
            draw(e);
        });
    })
}

export { brushMask, segmentMask }