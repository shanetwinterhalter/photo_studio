import { callModel } from "./serverRequests.js";
import { configureSidebarUi, updatePrompts } from "./sidebarUi.js";

function loadImageListeners() {
    // When upload button pressed
    $("#uploadImageForm").on("submit", function (event) {
        event.preventDefault();
        callModel("upload");
    });

    // When image generated
    $("#generateImageButton").on("click", function () {
        updatePrompts();
        callModel("generate");
    });
}

function editImageListeners() {
    // Request server to update image
    $("#inpaintButton").on("click", function() {
        callModel("inpaint");
    });

    // Upscale image
    $("#upscaleImageButton").on("click", function() {
        callModel("upscale");
    });
}

function configureSaveButton() {
    // On image saving
    $("#saveImageButton").on("click", function() {
        const imageSrc = $("#resultImage").attr("src");
        const filename = imageSrc.split("/").slice(-1)[0];
        const $link = $("<a></a>");
        $link.attr("href", imageSrc);
        $link.attr("download", filename);
        $("body").append($link);
        $link[0].click();
        $link.remove();
    });
}

export function configureSidebar() {
    // Set sidebar width
    configureSidebarUi();

    // Configure loading image
    loadImageListeners();

    // Configure prompting

    // Configure image editing
    editImageListeners();

    // Configure advanced options

    // Configure image saving
    configureSaveButton();
}