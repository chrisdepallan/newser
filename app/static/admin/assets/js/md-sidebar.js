document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    const toggleButton = document.querySelector(".md-sidebar .md-sidebar-toggle");
    const sidebarAside = document.querySelector(".md-sidebar .md-sidebar-aside");

    toggleButton.addEventListener("click", function (e) {
      sidebarAside.classList.toggle("open");
    });
  });