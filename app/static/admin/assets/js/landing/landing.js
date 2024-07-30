//landing header //
$(".toggle-menu").on("click", function () {
  $(".landing-menu").toggleClass("open");
});
$(".menu-back").on("click", function () {
  $(".landing-menu").toggleClass("open");
});
/*=====================
        02 Tap to top js
    ==========================*/
const button = document.querySelector(".tap-top");
const displayButton = () => {
  window.addEventListener("scroll", () => {
    if (window.scrollY > 600) {
      button.style.display = "block";
    } else {
      button.style.display = "none";
    }
  });
};
const scrollToTop = () => {
  button.addEventListener("click", () => {
    window.scroll({
      top: 0,
      left: 0,
      behavior: "smooth",
    });
    console.log(event);
  });
};
displayButton();
scrollToTop();
// tooltip
var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});
