$(function () {
  $(".modal").hide();
  var device;
  const main = document.getElementById("main");
  $.getJSON("/token")
    .then(function (data) {
      log("Got a token.");
      console.log("Token: " + data.token);

      device = new Twilio.Device(data.token, {
        codecPreferences: ["opus", "pcmu"],
        fakeLocalDTMF: true,
        enableRingingState: true,
        debug: true,
      });

      device.on("ready", function (device) {
        log("Twilio.Device Ready!");
      });

      device.on("error", function (error) {
        log("Twilio.Device Error: " + error.message);
      });

      device.on("connect", function (conn) {
        log("Successfully established call ! ");
        startTimer();
        main.className = "main-blurred";
        $("#modal-call-in-progress").show();
        console.log("CALLSID")
      });

      device.on("disconnect", function (conn) {
        log("Call ended.");
        main.className = "main";
        stopTimer();
        $(".modal").hide();
        console.log("HELOO")
        const sid = conn.parameters.CallSid;;
        $.post("/getCall", {
          sid: sid,
          from: empid,
          to: phone,
        }).done((data) => {
          console.log(data);
        });
        console.log(conn.parameters.callSid);
      });
    })
    .catch(function (err) {
      console.log(err);
      log("Could not get a token from server!");
    });

  $("#btnDial").bind("click", function () {
    var params = {
      To: phone,
    };

    $("#txtPhoneNumber").text(params.To);

    console.log("Calling " + params.To + "...");
    if (device) {
      var outgoingConnection = device.connect(params);
      outgoingConnection.on("ringing", function () {
        log("Ringing...");
      });
    }
  });

  $(".btnHangUp").bind("click", function () {
    $(".modal").hide();
    log("Hanging up...");
    if (device) {
      device.disconnectAll();
    }
  });

  function log(message) {
    console.log(message);
  }
});

var timer; // variable to hold the timer object
var totalSeconds = 0; // variable to hold the total number of seconds

function startTimer() {
  timer = setInterval(updateTimer, 1000); // start the timer
}

function stopTimer() {
  clearInterval(timer); // stop the timer
  timer = null;
  totalSeconds = 0;
  updateTimer();
}

function updateTimer() {
  var hours = Math.floor(totalSeconds / 3600);
  var minutes = Math.floor((totalSeconds - hours * 3600) / 60);
  var seconds = totalSeconds - hours * 3600 - minutes * 60;

  // add leading zeros to the time values
  if (hours < 10) {
    hours = "0" + hours;
  }
  if (minutes < 10) {
    minutes = "0" + minutes;
  }
  if (seconds < 10) {
    seconds = "0" + seconds;
  }

  document.getElementById("callDuration").innerHTML = minutes + ":" + seconds;

  totalSeconds++; // increment the total number of seconds
}
