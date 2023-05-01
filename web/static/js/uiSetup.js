import { resizeAndRecentreImage } from "./utils/uiUtils.js";

function configureSliders() {
    $('.form-range').each(function() {
        $(this).on('input', function() {
            const outputId = this.id.replace("Slider", "Value");
            $('#' + outputId).text(this.value);
        });
    });
}

function configureSidebarButtons() {
    // Select all buttons in the sidebar and attach a click event handler
    $("#uiSectionSelectors .selectable").on("click", function () {
        if ($(this).hasClass("selected-button")) {
            $(this).removeClass("selected-button");
        } else {
            $(this).addClass("selected-button");
        }
        displayUserOptions();
    });
}

function isAnyButtonSelected() {
    const buttons = $("#uiSectionSelectors .selectable");
    let isSelected = false;
    
    buttons.each((_, button) => {
      if ($(button).hasClass("selected-button")) {
        isSelected = true;
      }
    });
    return isSelected;
}

function displayUserOptions() {
    if (isAnyButtonSelected()) {
        $("#userOptions").show();
    } else {
        $("#userOptions").hide();
    }
    resizeAndRecentreImage();
}

function setUserOptionsWidth() {
    const userOptions = $("#userOptions");
    const children = userOptions.find(">");
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
    userOptions.css("min-width", maxWidth + "px");
    userOptions.hide();
}


export function setupUi() {
    // Updates label value for each slider
    configureSliders()

    // Handle how sidebar buttons look when clicked
    configureSidebarButtons()

    // Hide userOptions if no button selected
    displayUserOptions()

    // Configure userOptions width
    setUserOptionsWidth()
}