const config = {
    type: 'bar',
    data: {
        datasets: [{
            data: data,
            backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
            ],
            label: 'Ventes'
        }
        // Essayer pouvoir selectionner donné dans chart js avec formulaire
        // modifiant data et labels
        ],
        labels: labels
    },
    options: {
        responsive: true
    }
    };

const config2 = {
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
    var ctx = document.getElementById('bar-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
    var ctx2 = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctx2, config2);
    };
