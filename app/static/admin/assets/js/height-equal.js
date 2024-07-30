/*=====================
      Height Equal js
==========================*/


"use strict";
function equalizer() {
  var max = -1;
  $(".height_equal").css("min-height", "auto");
  $(".height_equal").each(function () {
    var minHeight = $(this).outerHeight();
    max = minHeight > max ? minHeight : max;
  });
  $(".height_equal").css("min-height", max);
  if ($(window).width() <= 991) {
    $(".height_equal").css("min-height", "auto");
  }

  $(".height_equal_2").css("min-height", "auto");
  $(".height_equal_2").each(function () {
    var minHeight = $(this).outerHeight();
    max = minHeight > max ? minHeight : max;
  });
  $(".height_equal_2").css("min-height", max);
  if ($(window).width() <= 991) {
    $(".height_equal_2").css("min-height", "auto");
  }
}
(function ($) {
  "use strict";
  equalizer();
})(jQuery);
jQuery(window).resize(function () {
  equalizer();
});
