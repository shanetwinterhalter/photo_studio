export function updateImage(imageUrl) {
    const img = $("#resultImage")
    img.attr("src", imageUrl);
    img.show();
}

export function disableUi(enable) {
    if (enable) {
        $("#loadedImageDisplay").show();
        $(".submitButton").prop("disabled", true);
        $("#loader").show();
    } else {
        $("#loader").hide();
        $(".submitButton").prop("disabled", false);
    }
}