// Fonctions
function creerDicoData(labels, data){
    var dicoData = {}
    var listeData = []
    var iData=-1
    for (elt in labels){
        for (elt2 in labels){
            iData+=1
            if (labels[elt] == labels[iData]){
                listeData.push(data1[iData])
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
dicoData1 = creerDicoData(labels1, data1)

// Créer le dicoData pour histogramme bar stacked2
dicoData2 = creerDicoData(labels2, data2)

// Créer la liste de data (presque) final pour histogramme bar stacked
var listDataFinal1 = creerListeDataFinal(dicoData1, labels1)

// Créer la liste de data (presque) final pour histogramme bar stacked 2
var listDataFinal2 = creerListeDataFinal(dicoData2, labels2)

// Data final à utiliser pour chart JS (histogramme bar stacked)
const dataFinal1 = {
    labels: labels1,
    datasets: listDataFinal1
}

// Data final à utiliser pour chart JS (histogramme bar stacked)
const dataFinal2 = {
    labels: labels2,
    datasets: listDataFinal2
}

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
        backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
        ],
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
        backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
        ],
        label: 'Population'
        }],
        labels: labels2
    },
    options: {
        responsive: true
    }
    };
    
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

        function zoomClick(click, chart, labels){
    
            var limiteYTop = chart.chartArea.top;
            var limiteYBottom = chart.chartArea.bottom;
    
            var limiteXRight = chart.chartArea.right;
            var limiteXLeft = chart.chartArea.left;
    
            var qteX = labels.length;
    
            var tailleBaton = ( limiteXRight - limiteXLeft ) / qteX
    
            for (elt in labels){
                elt = parseInt(elt);
                if (click.offsetY > limiteYTop && click.offsetY < limiteYBottom && click.offsetX > limiteXLeft + tailleBaton * elt && click.offsetX < limiteXLeft + tailleBaton * (elt+1)){
                    console.log(chart.data.labels[elt]);
                    console.log(chart.data.datasets[elt].data[elt]);
                }
            }
        }
        myChartH.canvas.addEventListener('click', (e) => {zoomClick(e, myChartH, labels1);
        })
        myChartH2.canvas.addEventListener('click', (e) => {zoomClick(e, myChartH2, labels2);
        })
    };
