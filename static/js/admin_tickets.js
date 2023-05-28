$("#loader_button").fadeOut();
$("#text").fadeIn();
$("#desc").fadeOut();

const showTicket = (ticketID) => {
  const box = $("#ticket_expanded");
  const main = document.getElementById("main");
  const ticket = document.getElementById("ticketID");
  const name = document.getElementById("name");
  const subject = document.getElementById("subject");
  const message = document.getElementById("message");
  const date = document.getElementById("date");
  const profile = document.getElementById("profile");
  const resolve = document.getElementById("resolve");

  $.post("/admin/activetickets", { id: ticketID, type: "request" }, (data) => {
    ticket.innerHTML = ticketID;
    name.innerHTML = data.name;
    subject.innerHTML = data.subject;
    message.innerHTML = data.message;
    date.innerHTML = "Received: " + data.created_at;

    profile.setAttribute(
      "onclick",
      `window.location.href = "customer/${data.profile}"`
    );
    resolve.setAttribute("onclick", `resolve_ticket(${ticketID})`);
  });

  box.fadeIn();
  main.className = "main-blurred";
};

const resolve = (ticketID) => {
  $("#desc").fadeIn();
  document.getElementById("ticket_expanded").className = "box_blurred";
};

const resolve_ticket = (ticketID) => {
  $("#text").fadeOut();
  $("#loader_button").delay(200).fadeIn();
  $.post(
    "/employee/activetickets",
    { id: ticketID, type: "resolve", desc: "Resolved by Admin" },
    (data) => {
      if (data) {
        $("#text").fadeIn();
        $("#loader_button").fadeOut();
        alert("Ticket Marked as Resolved Successfully");
        location.reload();
      }
    }
  );
};

const closeIn = () => {
  const box = $("#desc");
  const sec = document.getElementById("ticket_expanded");

  box.fadeOut();
  setTimeout(() => {
    sec.className = "ticket_expanded";
  }, 80);
};

const closeTicket = () => {
  const box = $("#ticket_expanded");
  const main = document.getElementById("main");

  box.fadeOut();
  setTimeout(() => {
    main.className = "main";
  }, 80);
};
