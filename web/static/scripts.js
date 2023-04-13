const brushSize = 10;

let canvas;
let ctx;
let img;
let painting = false;
let mask = null;

function updateImage(imageUrl, success) {
    $("#loader").hide();
    $("#resultImage").css("opacity", 1);
    //$("#canvas").css("opacity", 1);
    if (success) {
        img = $("#resultImage")
        img.attr("src", ""); // Clear image
        img.on("load", function() {
            configureCanvas(); // Configure canvas after image is loaded
            updateImageSize();
        });
        img.attr("src", imageUrl);
        img.show();
        $("#saveImageLink").attr("href", imageUrl);
        $("#saveImageLink").attr("download", imageUrl.split("/").slice(-1)[0]);
        generateSegmentMask(imageUrl);
    }
    // TODO: Re-add when running segmentation in parallel
    //$(".submitButton").prop("disabled", false);
}

function updateImageSize() {
    const content = document.getElementById('content');
    const image = document.getElementById('resultImage');
  
    image.style.maxWidth = `${content.clientWidth}px`;
    image.style.maxHeight = `${content.clientHeight}px`;
  }

// Brush tool
function startPosition(e) {
    painting = true;
    draw(e);
}

function finishedPosition() {
    painting = false;
    ctx.beginPath();
}

function draw(e, painting) {
    if (!painting) return;

    const canvasRect = canvas.getBoundingClientRect();
    const x = Math.floor(e.clientX - canvasRect.left);
    const y = Math.floor(e.clientY - canvasRect.top);

    ctx.lineWidth = brushSize;
    ctx.lineCap = "round";
    ctx.strokeStyle = "white";
    ctx.globalAlpha = 0.5; // 50% transparency

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

function configureCanvas() {
    canvas = $("#canvas")[0];
    ctx = canvas.getContext("2d");
    img = $("#resultImage")[0];

    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    ctx.drawImage(img, 0, 0);
    mask = new Array(img.naturalWidth * img.naturalHeight).fill(0);

    canvas.addEventListener("mousedown", startPosition);
    canvas.addEventListener("mouseup", finishedPosition);
    canvas.addEventListener("mousemove", function (e) {
        draw(e, painting);
    });
}

function setLoading() {
    $(".submitButton").prop("disabled", true);
    $("#loadedImageDisplay").show();
    $("#loader").show();
    $("#resultImage").css("opacity", 0.5);
    //$("#canvas").css("opacity", 0.5);
}

function upscaleImage() {
    setLoading();

    $.ajax({
        url: "/upscale_image",
        method: "POST",
        data: {
            image_url: $("#resultImage").attr("src")
        },
        success: function (response) {
            updateImage(response.image_url, true);
        },
        error: function (error) {
            console.error(error);
            updateImage("", false)
        }
    })
}

function generateSegmentMask(imageUrl) {
    $(".submitButton").prop("disabled", true);
    $.ajax({
        url: "/segment_image",
        method: "POST",
        data: {
            image_url: imageUrl
        },
        success: function (response) {
            $(".submitButton").prop("disabled", false);
            console.log(response.image_mask);
        },
        error: function (error) {
            $(".submitButton").prop("disabled", false);
            console.error(error);
        }
    })
    
}

function generateImage() {
    setLoading();

    $.ajax({
        url: "/generate_image",
        method: "POST",
        data: {
            prompt: $("#imgPrompt").val()
        },
        success: function (response) {
            updateImage(response.image_url, true);
        },
        error: function (error) {
            console.error(error);
            updateImage("", false)
        }
    })
}

function uploadImage() {
    const fileInput = document.getElementById("fileUpload");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to upload");
        return;
    }
    setLoading();
    
    const formData = new FormData();
    formData.append("image", file);

    $.ajax({
        url: "/upload_image",
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            updateImage(data.image_url, true);
        },
        error: function (jqXHR, textStatus, errorMessage) {
            console.error("Upload failed:", textStatus, errorMessage);
            updateImage("", false)
        }
    })
}

function maskToBinaryString(mask) {
    let binaryString = "";
    for (let i = 0; i < mask.length; i += 8) {
        let byte = 0;
        for (let j = 0; j < 8; j++) {
            byte |= (mask[i + j] << j);
        }
        binaryString += String.fromCharCode(byte);
    }
    return binaryString;
}

function binaryStringToBase64(binaryString) {
    return btoa(unescape(encodeURIComponent(JSON.stringify(mask))));
}

function inpaintImage() {
    setLoading();

    const maskBinaryString = maskToBinaryString(mask);
    const maskBase64 = binaryStringToBase64(maskBinaryString);

    console.log(maskBase64);

    $.ajax({
        url: "/inpaint_image",
        method: "POST",
        data: {
            image_url: $("#resultImage").attr("src"),
            mask: maskBase64
        },
        success: function (response) {
            updateImage(response.image_url, true);
        },
        error: function (error) {
            console.error(error);
            updateImage("", false)
        }
    })
}

function onGenerateSubmit(event) {
    event.preventDefault();
    generateImage();
}

function onUploadSubmit(event) {
    event.preventDefault();
    uploadImage();
}

$("#generateImageForm").submit(onGenerateSubmit);
$("#uploadImageForm").submit(onUploadSubmit);
window.addEventListener("resize", updateImageSize);