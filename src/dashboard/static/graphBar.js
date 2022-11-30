const config = {
    type: 'bar',
    data: {
        datasets: [{
            data: data,
            backgroundColor: [
            '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
            ],
            label: 'Ventes'
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
    };
