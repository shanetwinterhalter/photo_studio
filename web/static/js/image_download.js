export function configureSaveButton() {
    const imageSrc = $("#resultImage").attr("src");
    const downloadButton = $("#saveImageButton");
    const filename = imageSrc.split("/").slice(-1)[0];

    downloadButton.attr("download", filename);
    downloadButton.on("click", function() {
        const $link = $("<a></a>");
        $link.attr("href", imageSrc);
        $link.attr("download", filename);
        $("body").append($link);
        $link[0].click();
        $link.remove();
    });
}