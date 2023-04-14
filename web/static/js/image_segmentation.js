export function generateSegmentMask() {
    $.ajax({
        url: "/segment_image",
        method: "POST",
        data: {
            image_url: $("#resultImage").attr("src")
        },
        success: function (response) {
            console.log(response.image_mask);
        },
        error: function (error) {
            console.error(error);
        }
    })
}
