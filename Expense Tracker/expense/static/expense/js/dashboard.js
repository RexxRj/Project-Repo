document.addEventListener("DOMContentLoaded", function () {
  // Parse the categories and amounts from the data attributes
  const categories = JSON.parse(
    document.getElementById("chart-data").dataset.categories
  );
  const amounts = JSON.parse(
    document.getElementById("chart-data").dataset.amounts
  );
  const balances = JSON.parse(
    document.getElementById("chart-data").dataset.balances
  );

  const dates = JSON.parse(document.getElementById("chart-data").dataset.dates);

  const minValue = Math.min(...balances);
  const maxValue = Math.max(...balances);

  function roundToSignificant(value, step = 100000) {
    return Math.floor(value / step) * step;
  }

  const roundedMin = roundToSignificant(minValue);

  // Calculate a reasonable step size based on the range of values
  const range = maxValue - minValue;
  let stepSize = 100000; // Default step size

  // Adjust the step size based on the range
  if (range > 0 && range <= 1000000) {
    stepSize = 50000;
  } else if (range > 1000000 && range <= 5000000) {
    stepSize = 100000;
  } else if (range > 5000000) {
    stepSize = 5000000;
  }

  // Get the context of the canvas element for the pie chart
  const piectx = document
    .getElementById("transactionPieChart")
    .getContext("2d");
  const linectx = document
    .getElementById("transactionLineChart")
    .getContext("2d");

  function generateRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  const backgroundColors = categories.map(() => generateRandomColor());

  // Create the pie chart using Chart.js
  const pieChart = new Chart(piectx, {
    type: "pie", // Define the chart type (pie chart)
    data: {
      labels: categories, // Set the labels (categories)
      datasets: [
        {
          data: amounts, // Set the data (amounts)
          backgroundColor: backgroundColors, // Define colors
          borderColor: "#fff", // Border color for slices
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: false, // Make the chart responsive
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top", // Position of the legend
        },
        tooltip: {
          callbacks: {
            label: function (tooltipItem) {
              return `${tooltipItem.label}: ₹${tooltipItem.raw.toFixed(2)}`; // Format tooltips
            },
          },
        },
      },
    },
  });

  function getIsWeek(startDate, endDate) {
    const diffInMillis = endDate - startDate;
    const diffInDays = diffInMillis / (1000 * 60 * 60 * 24); // Convert to days

    let isWeek = 1; // Default to showing one label per day

    if (diffInDays > 60) {
      // For more than 2 months, show monthly intervals
      isWeek = 0; // Show every month
    }

    return isWeek;
  }

  const start = new Date(dates[0]);
  const end = new Date(dates[dates.length - 1]);

  // Get the step size based on the range
  const isWeek = getIsWeek(start, end);

  const lineChart = new Chart(linectx, {
    type: "line",
    data: {
      labels: dates, // Labels for the X-axis (can be hidden in options)
      datasets: [
        {
          data: balances, // Data for the chart
          borderColor: "rgba(75, 192, 192, 0.2)",
          backgroundColor: backgroundColors[0],
          borderWidth: 1,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: false, // Make the chart responsive
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: false, // Hide the legend
        },
      },
      scales: {
        x: {
          display: true, // Show X-axis
          title: {
            display: true,
            text: "Dates",
          },

          ticks: {
            maxTicksLimit: 10, // Limit the number of ticks displayed on the X-axis
            callback: function (value, index, values) {
              // If the value is a timestamp (in milliseconds), convert it to Date

              const date = new Date(dates[index]); // value is a timestamp
              if (isWeek) {
                return date.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                }); // Convert Date to 'MMM DD'
              }
              return date.toISOString().slice(0, 7); // Convert Date to 'YYYY-MM-DD'
            },
          },
        },
        y: {
          display: true, // Show the Y-axis
          title: {
            display: true,
            text: "Balance", // Add title to Y-axis
          },
          beginAtZero: true,
          min: roundedMin,
          ticks: {
            stepSize: stepSize, // Set the step size between Y-axis values
          },
        },
      },
    },
  });
});
