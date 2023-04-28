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

function showExtendedOptions() {
    if (isAnyButtonSelected()) {
        $("#userOptions").show();
    } else {
        $("#userOptions").hide();
    }
}

function setUserOptionsWidth() {
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

function configureSelectedButtons() {
    // Select all buttons in the sidebar and attach a click event handler
    $("#sidebar .btn").on("click", function () {
        if ($(this).hasClass("selected-button")) {
            $(this).removeClass("selected-button");
        } else {
            $(this).addClass("selected-button");
        }
        showExtendedOptions();
    });
}

export function updatePrompts() {
    $("#imgPrompt").val($("#imgPromptModal").val());
    $("#negativePrompt").val($("#negativePromptModal").val());
}

export function configureSidebarUi () {
    setUserOptionsWidth();
    configureSelectedButtons();
}