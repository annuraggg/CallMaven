const deleteItem = (id) => {
  $.post(`/admin/categories`, { type: "delete", id: id }).done((data) => {
    if (data.status === "success") {
      $(`#category-${id}`).remove();
    } else {
      alert("Error");
    }
  });
};

const add = $("#add");
add.hide();

const showModal = () => {
  const add = $("#add");
  const main = document.getElementById("main");
  add.fadeIn();
  main.className = "main-blurred";
};

const closeModal = () => {
  const add = $("#add");
  const main = document.getElementById("main");
  add.fadeOut();
  main.className = "main";
};

const submit = () => {
  const name = document.getElementById("name").value;
  const desc = document.getElementById("desc").value;

  $.post(`/admin/categories`, { type: "add", name: name, desc: desc }).done(
    (data) => {
      if (data.status === "success") {
        location.reload();
      } else {
        alert("Error");
      }
    }
  );
};
