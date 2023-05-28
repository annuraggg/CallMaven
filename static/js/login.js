loader = $("#loader");
loader.fadeOut();
submit = document.getElementById("submit");
err = document.getElementById("err");

submit.addEventListener("click", () => {
  event.preventDefault();
  id = document.getElementById("id").value;
  pw = document.getElementById("pw").value;
  loader.fadeIn();

  setTimeout(() => {
    $.post("/employee", {
      cid: id,
      pw: pw,
    }).done((data) => {
      console.log(data);
      if (data.auth == "True") {
        setTimeout(() => {
          err.innerHTML = "";
        }, 1000);
        document.cookie = `access_key=${data.token}`;
        window.location.href = "/employee/dashboard";
      } else if (data.auth == "False") {
        loader.delay(500).fadeOut();
        setTimeout(() => {
          err.innerHTML = "Wrong Username or Password";
        }, 1000);
      } else if (data.auth == "change") {
        loader.delay(500).fadeOut();

        $.post("/changepw", {
          cid: data.id,
        });
        
      } else {
        loader.delay(500).fadeOut();
        setTimeout(() => {
          err.innerHTML = "Something Went Wrong";
        }, 1000);
      }
    });
  }, 1500);
});
