// Modal
var dataFinalModal = produireDataFinal(dicoLabelsModal["United Kingdom"], dicoDataModal["United Kingdom"]);
var dicoDataFinalModal = {};
console.log("data ici=>",dicoDataModal)
console.log("labels ici=>",dicoLabelsModal)
for (elt in labels){
    dicoDataFinalModal[labels[elt]] = produireDataFinal(dicoLabelsModal[labels[elt]], dicoDataModal[labels[elt]]);
}
// Graph histogramme modal
const configBarModal = {
    type: 'bar',
    data: dataFinalModal,
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
var dicoModal = {}
console.log(dicoDataFinalModal)
$(document).ready(function() { /* code here */ 
      
    for (elt in labels){
        // Modal page graph Pays
        // var myModal = document.getElementById('myModal')
        // var myInput = document.getElementById('myInput')


        // Modal ------------
        // Histogramme
        // var ctxBarModal = document.getElementById('bar-chartModal'+labels[elt]).getContext('2d');
        new Chart(document.getElementById('bar-chartModal'+labels[elt]).getContext('2d'), {
            type: 'bar',
            data: dicoDataFinalModal[labels[elt]],
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
        });
        new Chart(document.getElementById('pie-chartModal'+labels[elt]).getContext('2d'), {
            type: 'pie',
            data: {
                datasets: [{
                    data: dicoDataModal[labels[elt]],
                    backgroundColor: [
                        '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
                    ],
                    label: 'Population'
                }],
                labels: dicoLabelsModal[labels[elt]]
            },
            options: {
                responsive: true
            }
        })
    }
});
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
    // console.log("heeeey",dicoData)
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
    // console.log(dicoData)
    return listDataFinal
}
function zoomClick(click, chart, labels){
    var listePaysInput = [];
    var i = -1;
    while (true){
        i +=1;
        try{
            var paysInput = document.getElementsByClassName("pays")[i].value;
            listePaysInput.push(paysInput);
        }
        catch{
            break;
        }
    }
    // console.log("pays", listePaysInput);

    // Algo click event V2
    var limiteYTop = chart.chartArea.top;
    var limiteYBottom = chart.chartArea.bottom;

    var limiteXRight = chart.chartArea.right;
    var limiteXLeft = chart.chartArea.left;

    var qteX = labels.length;

    var tailleBaton = ( limiteXRight - limiteXLeft ) / qteX

    // Boucle for permet d'analyser la position du click
    for (elt in labels){
        elt = parseInt(elt);
        if (click.offsetY > limiteYTop && click.offsetY < limiteYBottom && click.offsetX > limiteXLeft + tailleBaton * elt && click.offsetX < limiteXLeft + tailleBaton * (elt+1)){
            var valeurLabel = chart.data.labels[elt]
            // console.log("valeurLabel: ",valeurLabel);

            // Seulement si page graph ou produits
            if (document.getElementById("quelPage").innerText == "graphPays" || document.getElementById("quelPage").innerText == "graphProduits"){
                // ici faire chart update avec la nouvelle data correspondant au label selectionné
                // Ensuite affiche le modal

                document.getElementById("myBtn"+valeurLabel).click();
            }
        
            // Suite du code seulement si page graph3 
            if (document.getElementById("quelPage").innerText == "graph3"){
                if (listePaysInput.includes(valeurLabel)){
                    try{
                        document.getElementById("id_param2_1").value = valeurLabel;
                        document.getElementById("id_param1_1").value = 5; //À rendre dynamique
                        document.forms["form1"].submit();
                    }
                    catch(error){
                        // console.log(error);
                    }
                }
                else{
                    try{
                        document.getElementById("id_param2_2").value = valeurLabel;
                        document.getElementById("id_param1_2").value = 5; // À rendre dynamique
                        document.forms["form2"].submit();
                    }
                    catch(error){
                        // console.log(error);
                    }
                }
            }
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

// Les console.log
// console.log(myChartBarModal.data)
// console.log(dicoLabelsModal["United Kingdom"])
// console.log(dicoDataModal["United Kingdom"])
// console.log(dataFinalModal)