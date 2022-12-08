// Fonctions
function creerDicoData(labels, data){
    var dicoData = {}
    var listeData = []
    var iData=-1
    for (elt in labels){
        for (elt2 in labels){
            iData+=1
            if (labels[elt] == labels[iData]){
                listeData.push(data[iData])
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
function zoomClick(click, chart, labels){

    // Algo click event V2
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
function produireDataFinal(labels, data){
    // Créer le dicoData pour histogramme bar stacked
    dicoData = creerDicoData(labels, data)

    // Créer la liste de data (presque) final pour histogramme bar stacked
    var listDataFinal = creerListeDataFinal(dicoData, labels)

    // Data final à utiliser pour chart JS (histogramme bar stacked)
    const dataFinal = {
        labels: labels,
        datasets: listDataFinal
    }
    return dataFinal
}
