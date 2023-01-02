// Création des data pour chart JS

var dataFinal1 = produireDataFinal(labels1, data1, 1);
var dataFinal2 = produireDataFinal(labels2, data2, 2);

// Liste couleurs des graphs
var listeCouleurs1 = [
    '#2bc0a3',
    '#2b93c0',
    '#2b48c0',
    '#582bc0',
    '#a32bc0',
    '#c02b93'
]

var listeCouleurs2 = [
    '#c02b2b',
    '#c0762b',
    '#c0c02b',
    '#76c02b',
    '#2bc02b',
    '#2bc076'
]

// Graph histogramme 1
const configBar1 = {
    type: 'bar',
    data: dataFinal1,
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

// Graph camembert 1
const configPie1 = {
    type: 'pie',
    data: {
        datasets: [{
            data: data1,
            backgroundColor: listeCouleurs1,
            borderWidth: 1,
            label: 'Population'
        }],
        labels: labels1
    },
    options: {
        responsive: true
    }
};

// Graph histogramme 2
const configBar2 = {
    type: 'bar',
    data: dataFinal2,
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
    
// Graph camembert 2
const configPie2 = {
    type: 'pie',
    data: {
        datasets: [{
        data: data2,
        backgroundColor: listeCouleurs2,
        borderWidth: 1,
        label: 'Population'
        }],
        labels: labels2
    },
    options: {
        responsive: true
    }
};

// Afficher dans le HTML
window.onload = function() {
    // Histogramme 1
    var ctx = document.getElementById('bar-chart').getContext('2d');
    var myChartH = new Chart(ctx, configBar1);
    
    // Camembert 1
    var ctxPie = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctxPie, configPie1);

    // Histogramme 2
    var ctx2 = document.getElementById('bar-chart2').getContext('2d');
    var myChartH2 = new Chart(ctx2, configBar2);

    // Camembert 1
    var ctxPie2 = document.getElementById('pie-chart2').getContext('2d');
    window.myPie = new Chart(ctxPie2, configPie2);

    // Histogramme 1 cliquable
    myChartH.canvas.addEventListener('click', (e) => {actionClick(e, myChartH, labels1);
    })
    // Histogramme 2 cliquable
    myChartH2.canvas.addEventListener('click', (e) => {actionClick(e, myChartH2, labels2);
    })
};
