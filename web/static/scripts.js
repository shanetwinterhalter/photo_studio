function updateImage(imageUrl, success) {
    $("#loader").hide();
    if (success) {
        $("#resultImage").attr("src", imageUrl);
        $("#resultImage").show();
        $("#saveImageLink").attr("href", imageUrl);
        $("#saveImageLink").attr("download", imageUrl.split("/").slice(-1)[0]);
    }
    $(".submitButton").prop("disabled", false);
}

function setLoading() {
    $(".submitButton").prop("disabled", true);
    $("#loadedImageDisplay").show();
    $("#loader").show();
    $("#resultImage").hide();
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
    setLoading();

    const fileInput = document.getElementById("fileUpload");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please choose a file.");
        return;
    }

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