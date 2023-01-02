const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

var randomColor = Math.floor(Math.random()*16777215).toString(16);
var color = "#"+randomColor

listeData = []
indice = -1
for(elt in listePays){
    indice +=1
    listeData.push({
        label: listePays[indice],
        data: dicoData[listePays[indice]],
        backgroundColor: "#"+Math.floor(Math.random()*16777215).toString(16),
        stack: 'Stack 0'
    })
}
const data = {
  labels: labels,
  datasets: listeData
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

  // Afficher dans le HTML
  window.onload = function() {
    var ctx = document.getElementById('bar-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
    };