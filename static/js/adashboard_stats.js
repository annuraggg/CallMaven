// ! CHART ONE

// Create the chart

$.post("/apis/admin/chart1", {}).done((data) => {
  const dates = [];
  var formdates = [];

  for (let i = 0; i < 6; i++) {
    const date = new Date(Date.now() - i * 86400000)
      .toISOString()
      .substring(0, 10);
    dates.push(date);
    formdates.unshift(date);
  }

  today_chart = 0;
  oneday = 0;
  twoday = 0;
  threeday = 0;
  fourday = 0;
  fiveday = 0;
  for (const element of data) {
    const element1 = new Date(element);
    const dateString = element1.toISOString().substring(0, 10);
    const formDateStrings = dates;
    switch (dateString) {
      case formDateStrings[5]:
        today_chart++;
        break;
      case formDateStrings[4]:
        oneday++;
        break;
      case formDateStrings[3]:
        twoday++;
        break;
      case formDateStrings[2]:
        threeday++;
        break;
      case formDateStrings[1]:
        fourday++;
        break;
      case formDateStrings[0]:
        fiveday++;
        break;
    }
  }

  var chart1 = document.getElementById("chart1").getContext("2d");
  var chart1 = new Chart(chart1, {
    type: "bar",
    data: {
      labels: [dates[5], dates[4], dates[3], dates[2], dates[1], dates[0]],
      datasets: [
        {
          label: "Calls",
          data: [today_chart, oneday, twoday, threeday, fourday, fiveday],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(255, 99, 132, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(255, 99, 132, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: false,
    },
  });
});

// ! SECOND CHART

$.post("/apis/admin/chart2", {}).done((data) => {
  const dates = [];

  for (let i = 0; i < 6; i++) {
    const date = new Date(Date.now() - i * 86400000)
      .toISOString()
      .substring(0, 10);
    dates.push(date);
  }

  today_chart = 0;
  oneday = 0;
  twoday = 0;
  threeday = 0;
  fourday = 0;
  fiveday = 0;
  for (const element of data) {
    const element1 = new Date(element);
    const dateString = element1.toISOString().substring(0, 10);
    if (dateString == dates[0]) {
      today_chart++;
    } else if (dateString == dates[1]) {
      oneday++;
    } else if (dateString == dates[2]) {
      twoday++;
    } else if (dateString == dates[3]) {
      threeday++;
    } else if (dateString == dates[4]) {
      fourday++;
    } else if (dateString == dates[5]) {
      fiveday++;
    }
  }

  var chart2 = document.getElementById("chart2").getContext("2d");
  var chart2 = new Chart(chart2, {
    type: "bar",
    data: {
      labels: [dates[5], dates[4], dates[3], dates[2], dates[1], dates[0]],
      datasets: [
        {
          label: "Tickets",
          data: [fiveday, fourday, threeday, twoday, oneday, today_chart],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(255, 99, 132, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(255, 99, 132, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
});
