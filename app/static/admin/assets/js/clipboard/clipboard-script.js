document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    // Add click event listeners to copy buttons
    var copyButtons = document.querySelectorAll(".btn-clipboard");
    copyButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var textToCopy = button.getAttribute("data-clipboard-text");
        copyToClipboard(textToCopy, "copy");
      });
    });

    // Add click event listeners to cut buttons
    var cutButtons = document.querySelectorAll(".btn-clipboard-cut");
    cutButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var textToCut = button.getAttribute("data-clipboard-text");
        copyToClipboard(textToCut, "cut");
      });
    });

    // Function to copy text to clipboard
    function copyToClipboard(text, action) {
      var textArea = document.createElement("textarea");
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand(action === "copy" ? "copy" : "cut");
      document.body.removeChild(textArea);

      handleClipboardSuccess(action);
    }

    // Function to handle clipboard success event
    function handleClipboardSuccess(action) {
      if (action === "copy") {
        alert("copied");
      } else if (action === "cut") {
        alert("cut");
      }
    }
  });