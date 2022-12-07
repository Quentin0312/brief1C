// Graph histogramme 1
const configBar = {
    type: 'bar',
    data: {
        datasets: [{
            data: data,
            backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
            ],
            label: 'Ventes'
        }
        // Essayer pouvoir selectionner données dans chart js avec formulaire
        // modifiant data et labels
        ],
        labels: labels
    },
    options: {
        responsive: true
    }
    };
// Graph camembert 1
const configPie = {
    type: 'pie',
    data: {
        datasets: [{
        data: data,
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
