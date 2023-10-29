document.addEventListener("DOMContentLoaded", function () {
  const habits = ["Program"];

  function daysInMonth(month, year) {
    return new Date(year, month, 0).getDate();
  }

  function updateTableHeaders(month, year) {
    console.log("Updating headers..."); // debug log
    const days = daysInMonth(month, year);
    const thead = document.querySelector("#habit-tracker thead tr");

    while (thead.children.length > 1) {
      thead.removeChild(thead.lastChild);
    }

    for (let day = 1; day <= days; day++) {
      let th = document.createElement("th");
      th.textContent = day.toString();
      thead.appendChild(th);
    }
  }

  function populateCalendar(month, year) {
    console.log("Populating calendar..."); //debug log
    updateTableHeaders(month, year);
    const calendarBody = document.querySelector("#habit-tracker tbody");
    const daysInMonth = new Date(year, month, 0).getDate();

    calendarBody.innerHTML = "";

    for (let day = 1; day <= daysInMonth; day++) {
      let row = calendarBody.insertRow();

      let habitCell = row.instertCell();
      habitCell.textContent = habit;

      for (let day = 1; day <= daysInMonth; day++) {
        row.insertCell();
      }
    }
  }

  populateCalendar(10, 2023);
});
