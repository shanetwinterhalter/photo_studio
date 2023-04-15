let canvas;
let img;
let ctx;
let mask;
let painting = false;
const brushSize = 10; // Set your desired brush size

let toolMode = "brush";

// Brush tool
function startPosition(e) {
    painting = true;

    if (toolMode === "brush") {
        draw(e);
    } else if (toolMode === "segMasks") {
        applyPredefinedMask(e)
    }
}

function finishedPosition() {
    painting = false;
    ctx.beginPath();
}

function draw(e) {
    if (!painting) return;

    const canvasRect = $("#canvas")[0].getBoundingClientRect();
    const x = Math.floor(e.clientX - canvasRect.left);
    const y = Math.floor(e.clientY - canvasRect.top);

    ctx.lineWidth = brushSize;
    ctx.lineCap = "round";
    ctx.strokeStyle = "white";
    ctx.globalAlpha = 0.75; // 50% transparency

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);

    for (let i = -brushSize; i < brushSize; i++) {
        for (let j = -brushSize; j < brushSize; j++) {
            if (i * i + j * j < brushSize * brushSize) {
                const index = (y + j) * img.naturalWidth + (x + i);
                if (index >= 0 && index < mask.length) {
                    mask[index] = 1;
                }
            }
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
        ctx.drawImage(img, 0, 0);
        mask = new Array(img.naturalWidth * img.naturalHeight).fill(0);
    
        canvas.addEventListener("mousedown", startPosition);
        canvas.addEventListener("mouseup", finishedPosition);
        canvas.addEventListener("mousemove", function (e) {
            if (toolMode === "brush") {
                draw(e);
            }
        });
    })
}

export { mask };