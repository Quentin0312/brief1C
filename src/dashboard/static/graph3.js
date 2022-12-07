// Graph histogramme 1
const configBar1 = {
    type: 'bar',
    data: {
        datasets: [{
            data: data1,
            backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
            ],
            label: 'Ventes'
        }
        // Essayer pouvoir selectionner données dans chart js avec formulaire
        // modifiant data et labels
        ],
        labels: labels1
    },
    options: {
        responsive: true
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
    data: {
        datasets: [{
            data: data2,
            backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
            ],
            label: 'Ventes'
        }
        // Essayer pouvoir selectionner données dans chart js avec formulaire
        // modifiant data et labels
        ],
        labels: labels2
    },
    options: {
        responsive: true
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
        window.myPie = new Chart(ctx, configBar1);
        
        // Camembert 1
        var ctxPie = document.getElementById('pie-chart').getContext('2d');
        window.myPie = new Chart(ctxPie, configPie1);

        // Histogramme 2
        var ctx2 = document.getElementById('bar-chart2').getContext('2d');
        window.myPie = new Chart(ctx2, configBar2);

        // Camembert 1
        var ctxPie2 = document.getElementById('pie-chart2').getContext('2d');
        window.myPie = new Chart(ctxPie2, configPie2);
    };
