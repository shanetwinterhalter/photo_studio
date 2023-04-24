function isAnyButtonSelected() {
    const buttons = $("#sidebar .btn");
    let isSelected = false;
    
    buttons.each((_, button) => {
      if ($(button).hasClass("selected-button")) {
        isSelected = true;
      }
    });
    return isSelected;
}

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

export function setUserOptionsWidth() {
    const userOptions = $("#userOptions");
    const children = userOptions.find(".user-input-section");
    let maxWidth = 0;
    userOptions.show();
  
    children.each((_, child) => {
      const $child = $(child);
      $child.css("display", "block"); // Temporarily display the element to measure its width
      const childWidth = $child[0].getBoundingClientRect().width;
      if (childWidth > maxWidth) {
        maxWidth = childWidth;
      }
      $child.css("display", ""); // Reset display property
    });
    userOptions.css("width", maxWidth + "px");
    userOptions.hide();
}

export function checkSidebarConfiguration() {
    if (isAnyButtonSelected()) {
        $("#userOptions").show();
    } else {
        $("#userOptions").hide();
    }
}