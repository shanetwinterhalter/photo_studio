export function generateSegmentMask() {
    $("#maskIcon").prop("disabled", true);
    
    $.ajax({
        url: "/segment_image",
        method: "POST",
        data: {
            image_url: $("#resultImage").attr("src")
        },
        success: function (response) {
            console.log(response.image_mask);
            $("#maskIcon").prop("disabled", false);
        },
        error: function (error) {
            console.error(error);
            $("#maskIcon").prop("disabled", false);
        }
    })
}
