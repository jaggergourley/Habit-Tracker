$(document).ready(function () {
  $("#add-habit-btn").click(function () {
    const name = $("#name").val();
    const description = $("#description").val();
    $.post(
      "/add-habit",
      { name: name, description: description },
      function (data) {
        const habit = data;
        const newHabitHtml = `
            <li data-id="${habit.id}">
                ${habit.name} - ${habit.description} (Completed 0 times)
                <button class="complete-habit-btn">Mark as Completed</button>
                <button class="delete-habit-btn">Delete</button>
            </li>
            `;
        $("#habits-list").append(newHabitHtml);
      }
    );
  });

  $(document).on("click", ".complete-habit-btn", function () {
    const habitId = $(this).parent().data("id");
    $.post(`/complete-habit/${habitId}`, function () {
      location.reload();
    });
  });

  $(document).on("click", ".delete-habit-btn", function () {
    const habitId = $(this).parent().data("id");
    $.post(`/delete-habit/${habitId}`, function () {
      $(`li[data-id='${habitId}']`).remove();
    });
  });
});
