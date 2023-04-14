export function resizeImage() {
    const content = document.getElementById('content');
    const image = document.getElementById('resultImage');
  
    image.style.maxWidth = `${content.clientWidth}px`;
    image.style.maxHeight = `${content.clientHeight}px`;
}
export function updateImage(imageUrl) {
    const img = $("#resultImage")
    img.attr("src", imageUrl);
    img.on("load", function() {
        resizeImage();
    });
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