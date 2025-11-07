// chart 1

// var ctx = document.getElementById("chart-bars").getContext("2d");
//
// new Chart(ctx, {
//   type: "bar",
//   data: {
//     labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
//     datasets: [
//       {
//         label: "Sales",
//         tension: 0.4,
//         borderWidth: 0,
//         borderRadius: 4,
//         borderSkipped: false,
//         backgroundColor: "#fff",
//         data: [450, 200, 100, 220, 500, 100, 400, 230, 500],
//         maxBarThickness: 6,
//       },
//     ],
//   },
//   options: {
//     responsive: true,
//     maintainAspectRatio: false,
//     plugins: {
//       legend: {
//         display: false,
//       },
//     },
//     interaction: {
//       intersect: false,
//       mode: "index",
//     },
//     scales: {
//       y: {
//         grid: {
//           drawBorder: false,
//           display: false,
//           drawOnChartArea: false,
//           drawTicks: false,
//         },
//         ticks: {
//           suggestedMin: 0,
//           suggestedMax: 600,
//           beginAtZero: true,
//           padding: 15,
//           font: {
//             size: 14,
//             family: "Open Sans",
//             style: "normal",
//             lineHeight: 2,
//           },
//           color: "#fff",
//         },
//       },
//       x: {
//         grid: {
//           drawBorder: false,
//           display: false,
//           drawOnChartArea: false,
//           drawTicks: false,
//         },
//         ticks: {
//           display: false,
//         },
//       },
//     },
//   },
// });

// end chart 1
window.addEventListener("DOMContentLoaded", function () {
  const blocks = document.querySelectorAll('.currency-block');
  const dataPoints = [];

  blocks.forEach(block => {
    const currencyEl = block.querySelector('[data-currency]');
    const amountEl = block.querySelector('[data-amount]');



    if (currencyEl && amountEl) {
      const currency = currencyEl.dataset.currency;
      const amount = parseFloat(amountEl.dataset.amount);

      if (!isNaN(amount)) {
        dataPoints.push({ label: currency, y: amount });
      }
    }
  });

  if (dataPoints.length === 0) {
    console.warn("No currency data found for chart.");
    return;
  }

  const chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    title: {
      text: "Розподіл коштів за валютами"
    },
    data: [{
      type: "pie",
      startAngle: 240,
      yValueFormatString: "#,##0.00\"\"",
      indexLabel: "{label}: {y}",
      dataPoints: dataPoints
    }]
  });


  chart.render();
});
