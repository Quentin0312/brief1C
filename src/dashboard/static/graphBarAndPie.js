// Fonctions
function creerDicoData(labels, data){
    var dicoData = {}
    var listeData = []
    var iData=-1
    for (elt in labels){
        for (elt2 in labels){
            iData+=1
            if (labels[elt] == labels[iData]){
                listeData.push(data0[iData])
            }
            else{
                listeData.push(0)
            }
        }
        dicoData[labels[elt]] = listeData
        listeData = []
        iData=-1
    }
    return dicoData 
}
function creerListeDataFinal(dicoData, labels){
    var listDataFinal = []
    var i2 = -1
    for (elt in dicoData){
        i2 += 1
        listDataFinal.push({
            label: labels[i2],
            data : dicoData[labels[i2]],
            backgroundColor: "#"+Math.floor(Math.random()*16777215).toString(16),
            stack: 'Stack 0'
        })
    }
    console.log(dicoData)
    return listDataFinal
}

// Créer le dicoData pour histogramme bar stacked
dicoData = creerDicoData(labels, data0)

// Créer la liste de data (presque) final pour histogramme bar stacked
var listDataFinal = creerListeDataFinal(dicoData, labels)

// Data final à utiliser pour chart JS (histogramme bar stacked)
const dataFinal = {
    labels: labels,
    datasets: listDataFinal
}

// Graph histogramme
const configBar = {
    type: 'bar',
    data: dataFinal,
    options: {
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

// Fonction onclick
function clickhandler(click){
    const points = myChart.getElementsAtEventForMode
}


// Afficher dans le HTML
window.onload = function() {
    // Histogramme
    var ctx = document.getElementById('bar-chart').getContext('2d');
    var myChart = new Chart(ctx, configBar);
    
    // Camembert
    var ctxPie = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctxPie, configPie);

    // Fonction onclick
    // function clickhandler(click){
    //     const points = window.myPie.getElementsAtEventForMode(click, 'nearest', {intersect: true}, true);
    //     if (points.length){
    //         console.log(points.length)
    //     }
    // }
    // ctx.onclick = clickhandler;

    //Test 2 
    function zoomClick(click, chart){
        // Tuto YTB à garder au cas ou
        // chart.config.options.scales.x.min = 2;
        // chart.config.options.scales.x.max = 4;
        // chart.update();

        // Proportion sur le canva de la marge de gauche
        var proportionXMarge = 0.11;
        // Len labels
        var qteX = labels.length;
        // Largeur du canva
        var longueurXCanva = ctx.canvas.width;
        // Largeur de la marge de gauche
        var longueurXMarge = longueurXCanva*proportionXMarge;
        // Largeur d'une colonne d'un histogramme
        var tailleBaton = longueurXCanva * (1 - proportionXMarge) / qteX;

        for (elt in labels){
            elt = parseInt(elt)
            var eltPlus = elt + 1
            if (click.offsetX > (longueurXMarge + tailleBaton*elt) && click.offsetX < (longueurXMarge + tailleBaton * eltPlus) && click.offsetY > myChart.chartArea.top && click.offsetY < myChart.chartArea.bottom){
                // console.log(chart.data.labels[elt]);
                // console.log(chart.data.datasets[elt].data[elt]);
                console.log(myChart.chartArea.bottom);
                console.log(click.offsetY)
            }
        }
    }

    myChart.canvas.addEventListener('click', (e) => {zoomClick(e, myChart);
    })

};
