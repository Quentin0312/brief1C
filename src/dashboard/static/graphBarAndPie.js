// Création des data pour chart JS
var dataFinal = produireDataFinal(labels, data0,0);

// Liste couleurs des graphs
var listeCouleurs = [
    '#2bc0a3',
    '#2b93c0',
    '#2b48c0',
    '#582bc0',
    '#a32bc0',
    '#c02b93',
    '#c02b2b',
    '#c0762b',
    '#c0c02b',
    '#76c02b',
    '#2bc02b',
    '#2bc076'
]
var couleursTest = [
    '#36A2EB',
    '#FF6384',
    '#4BC0C0',
    '#FF9F40',
    '#9966FF',
    '#FFCD56',
    '#C9CBCF'

]

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
        backgroundColor: listeCouleurs,
        borderWidth: 1,
        label: 'Population'
        }],
        labels: labels
    },
    options: {
        responsive: true
    }
};
// console.log("laa",dataFinal)



// Afficher dans le HTML
window.onload = function() {
    // Histogramme
    var ctx = document.getElementById('bar-chart').getContext('2d');
    var myChart = new Chart(ctx, configBar);
    
    // Camembert
    var ctxPie = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctxPie, configPie);

    // Histogramme cliquable
    myChart.canvas.addEventListener('click', (e) => {actionClick(e, myChart, labels);
    })


    // Camembert

    // myModal.addEventListener('shown.bs.modal', function () {
    //     myInput.focus()
    // }) 

};