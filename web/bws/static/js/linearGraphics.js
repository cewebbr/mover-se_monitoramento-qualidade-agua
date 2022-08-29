var nameSensor = document.getElementById('name-sensor').innerText
var valueSensor =  JSON.parse(document.getElementById('list-sensor-value').value)


var options = {
    series: [{
        name: nameSensor,
        data: valueSensor
    }],
    chart: {
        height: 320,
        type: 'line',
        zoom: {
            enabled: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'straight'
    },
    markes : {
        size: 0
    },
    xaxis: {
        categories: ['']
    },
    grid: {
        row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
        },
    },

};

var linearGraphic = document.getElementById('graphic-linear')
var chart = new ApexCharts(linearGraphic, options);
chart.render();
