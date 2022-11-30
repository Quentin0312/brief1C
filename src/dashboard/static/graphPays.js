const config = {
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
    var ctx = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
    };
