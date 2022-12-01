const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

// const labels = [1,2,3,4,5,6,7]
const data = {
  labels: labels,
  datasets: [
    {
      label: 'Pays 1',
      data: dataTest,
      backgroundColor: '#696969',
      stack: 'Stack 0'
    },
    {
        label:'Pays 2',
        data: [3,2,5],
        backgroundColor: '#D3D3D3',
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