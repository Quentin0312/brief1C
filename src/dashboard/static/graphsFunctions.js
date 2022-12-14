// Info : Ce fichier JS fait:
// - Gestion des modals page graph pays et page graph produit ( Partie: Modal )
// - Contient toutes les fonctions à réutiliser dans tout les fichiers JS ( Partie: Fonctions )


// Modal -----------------------------------------------------------------------------------------------------------------------------

// Modal datasets
var dicoDataFinalModal = {};

// Rempli datasets avec les valeurs selon la page affiché (donc elt dans labels)
for (elt in labels){
    dicoDataFinalModal[labels[elt]] = produireDataFinal(dicoLabelsModal[labels[elt]], dicoDataModal[labels[elt]]);
}

// Concerne les graphs modal, il faut attendre que le HTML produit tout les modal contenant les canvas 
$(document).ready(function() {
    
    // Boucle pour pouvoir config dynamiquement les graphs modal
    for (elt in labels){

        // Configuration des charts histogramme modal
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

        // Configuration des charts pie modal
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

// Fonctions -------------------------------------------------------------------------------------------------------------------------

// Créer la liste de datas pour graph histogramme truqué pour la mise à l'echelle dynamique ex=>[0,0,0,0,1542,0,0]
function creerDicoData(labels, data){
    
    // Dictionnaire contenant les listes de data. Objectif : pouvoir utiliser les datas dynamiquement ex: for elt ; data = dicoData["elt"]
    var dicoData = {};
    
    // Contient une liste des datas d'une serie histogramme stacked
    var listeData = [];

    // Permet de construire une liste datas comme [0,0,0,0,1542,0,0] pour chart JS
    var iData=-1;
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
        // Liste data terminé injecté dans le dictionnaire
        dicoData[labels[elt]] = listeData

        // Réinit pour la liste suivante
        listeData = []
        iData=-1
    }
    return dicoData 
}

// Créer la data final pour la configuration du chart (dans la config=> {data: "creerConfigDataFinal(dicoData, labels)"})
function creerConfigDataFinal(dicoData, labels){

    // Liste contenant les dictionnaire data contenant {label:..., data:..., backgroundColor:..., stack:...}
    var listDataFinal = []

    // Permet de faire correspondre le bon labels et dicoData
    var i2 = -1
    // Permet de créer toute les series de datas
    for (elt in dicoData){
        i2 += 1
        listDataFinal.push({
            label: labels[i2],
            data : dicoData[labels[i2]],
            backgroundColor: "#"+Math.floor(Math.random()*16777215).toString(16),
            stack: 'Stack 0'
        })
    }
    return listDataFinal
}

// Permet d'afficher le bon modal selon la zone cliqué du graph histo
function actionClick(click, chart, labels){

    // Définit la liste des pays (existant dans la BDD) via la liste d'inputs du forms
    // Ne concerne que la page graph 3
    if (document.getElementById("quelPage").innerText == "graph3"){
        var listePaysInput = [];
        // Permet de push dans la liste tout les pays
        var i = -1;
        while (true){
            i +=1;

            // Try catch necessaire ici car break quand l'indice suivant (après le dernier) ne fonctionne pas
            try{
                // Récup du pays correspondant à l'indice
                var paysInput = document.getElementsByClassName("pays")[i].value;

                // Push ce pays dans la listePaysInput
                listePaysInput.push(paysInput);
            }
            catch (error){
                // console.log pas necessaire car error prévu pour déclencher le break !
                // console.log(error)
                break;
            }
        }
    }

// Code cleaned jusqu'içi -----------------------------------------------------------------------------------------------------------

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
                        console.log(error);
                    }
                }
                else{
                    try{
                        document.getElementById("id_param2_2").value = valeurLabel;
                        document.getElementById("id_param1_2").value = 5; // À rendre dynamique
                        document.forms["form2"].submit();
                    }
                    catch(error){
                        console.log(error);
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
    var configDataFinal = creerConfigDataFinal(dicoData, labels)

    // Data final à utiliser pour chart JS (histogramme bar stacked)
    const dataFinal = {
        labels: labels,
        datasets: configDataFinal
    }
    return dataFinal
}

// Les console.log
// console.log(myChartBarModal.data)
// console.log(dicoLabelsModal["United Kingdom"])
// console.log(dicoDataModal["United Kingdom"])
