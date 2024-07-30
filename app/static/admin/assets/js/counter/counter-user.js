document.addEventListener("DOMContentLoaded", () => {
    function counter(id, start, end, duration) {
     let obj = document.getElementById(id),
      current = start,
      range = end - start,
      increment = end > start ? 1 : -1,
      step = Math.abs(Math.floor(duration / range)),
      timer = setInterval(() => {
       current += increment;
       obj.textContent = current;
       if (current == end) {
        clearInterval(timer);
       }
      }, step);
    }
    counter("count2", 2000, 2659, 1000);
    counter("count3", 0, 569, 1000);
    counter("count6", 2000, 2659, 1000);
    counter("count7", 0, 569, 1000);
    counter("count8", 2000, 2659, 1000);
    counter("count9", 0, 569, 1000);
    counter("count10", 2000, 2659, 1000);
    counter("count11", 0, 569, 1000);
    counter("count4", 25000, 25869, 2000);
    counter("count5", 659700, 659887, 2000);
   });
   