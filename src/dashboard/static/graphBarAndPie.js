// Modif data pour histogramme truqué
dicoData = {}
listeData = []
iParam=-1
iData=-1
for (elt in labels){
    iParam+=1
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
listDataFinal = []
i2 = -1
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
const dataFinal = {
    labels: labels,
    datasets: listDataFinal
}
// Graph histogramme 1
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
// Graph camembert 1
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

    window.onload = function() {
        // Histogramme
        var ctx = document.getElementById('bar-chart').getContext('2d');
        window.myPie = new Chart(ctx, configBar);
        
        // Camembert
        var ctxPie = document.getElementById('pie-chart').getContext('2d');
        window.myPie = new Chart(ctxPie, configPie);
    };
