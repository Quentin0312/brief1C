const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

// const labels = [1,2,3,4,5,6,7]
const data = {
  labels: labels,
  datasets: [
    {
      label: listePays[0],
      data: dicoData[listePays[0]],
      backgroundColor: 'blue',
      stack: 'Stack 0'
    },
    {
        label: listePays[1],
        data: dicoData[listePays[1]],
        backgroundColor: 'red',
        stack: 'Stack 0'
    },
    {
        label: listePays[5],
        data: dicoData[listePays[5]],
        backgroundColor: 'green',
        stack: 'Stack 0'
    }
  ]
};

const config = {
    type: 'bar',
    data: data,
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Chart.js Bar Chart - Stacked'
        },
      },
      responsive: true,
      scales: {
        x: {
          stacked: true,
          grid: {
            offset: true
          }
        },
        y: {
          stacked: true
        }
      }
    }
  };
  window.onload = function() {
    var ctx = document.getElementById('bar-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
    };