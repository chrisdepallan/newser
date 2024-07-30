(function () {
  document.addEventListener("DOMContentLoaded", function () {
    var containerEl = document.getElementById("external-events-list");
    new FullCalendar.Draggable(containerEl, {
      itemSelector: ".fc-event",
      eventData: function (eventEl) {
        return {
          title: eventEl.innerText.trim(),
        };
      },
    });
    var calendarEl = document.getElementById("calendar");
    var calendar = new FullCalendar.Calendar(calendarEl, {
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
      },
      initialView: "dayGridMonth",
      initialDate: "2024-06-12",
      navLinks: true,
      editable: true,
      selectable: true,
      nowIndicator: true,
      events: [
        {
          title: "All Day Event",
          start: "2024-06-01",
        },
        {
          title: "Tour with our Team.",
          start: "2024-06-07",
          end: "2024-06-10",
        },
        {
          groupId: 999,
          title: "Meeting with Team",
          start: "2024-06-06T16:00:00",
        },
        {
          groupId: 999,
          title: "Upload New Project",
          start: "2024-06-16T16:00:00",
        },
        {
          title: "Birthday Party",
          start: "2024-06-24",
          end: "2024-06-26",
        },
        {
          title: "Reporting about Theme",
          start: "2024-06-28T10:30:00",
          end: "2024-06-29T12:30:00",
        },
        {
          title: "Lunch",
          start: "2024-06-30T12:00:00",
        },
        {
          title: "Meeting",
          start: "2024-06-12T14:30:00",
        },
        {
          title: "Happy Hour",
          start: "2024-06-30T17:30:00",
        },
      ],
      editable: true,
      droppable: true,
      drop: function (arg) {
        if (document.getElementById("drop-remove").checked) {
          arg.draggedEl.parentNode.removeChild(arg.draggedEl);
        }
      },
    });
    calendar.render();
  });
})();