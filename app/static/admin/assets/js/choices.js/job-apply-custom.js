
  document.addEventListener('DOMContentLoaded', function() {
    new Choices('#choices-scrolling-dropdown', {
        allowHTML: true,
        shouldSort: false,
      });  
      new Choices('#choices-scrolling-dropdown2', {
        allowHTML: true,
        shouldSort: false,
      });  
      new Choices('#choices-scrolling-dropdown3', {
        allowHTML: true,
        shouldSort: false,
      });
      new Choices('#choices-scrolling-dropdown4', {
        allowHTML: true,
        shouldSort: false,
      });
      new Choices('#choices-scrolling-dropdown5', {
        allowHTML: true,
        shouldSort: false,
      });
      var picker = new Pikaday({ field: document.getElementById('datepicker2') });
      var picker = new Pikaday({ field: document.getElementById('datepicker3') });
      var picker = new Pikaday({ field: document.getElementById('datepicker4') });
});