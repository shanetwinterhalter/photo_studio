export function configureSaveButton() {
    const imageSrc = $("#resultImage").attr("src");
    const filename = imageSrc.split("/").slice(-1)[0];
    const $link = $("<a></a>");
    $link.attr("href", imageSrc);
    $link.attr("download", filename);
    $("body").append($link);
    $link[0].click();
    $link.remove();
}