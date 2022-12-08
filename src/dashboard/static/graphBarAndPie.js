// Création des data pour chart JS
var dataFinal = produireDataFinal(labels, data0);

// Graph histogramme
const configBar = {
    type: 'bar',
    data: dataFinal,
    options: {
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

// Graph camembert
const configPie = {
    type: 'pie',
    data: {
        datasets: [{
        data: data0,
        backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
        ],
        label: 'Population'
        }],
        labels: labels
    },
    options: {
        responsive: true
    }
};


// Afficher dans le HTML
window.onload = function() {
    // Histogramme
    var ctx = document.getElementById('bar-chart').getContext('2d');
    var myChart = new Chart(ctx, configBar);
    
    // Camembert
    var ctxPie = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctxPie, configPie);

    // Histogramme cliquable
    myChart.canvas.addEventListener('click', (e) => {zoomClick(e, myChart, labels);
    })

};