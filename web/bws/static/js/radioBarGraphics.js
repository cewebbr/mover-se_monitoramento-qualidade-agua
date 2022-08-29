var valueNode = document.querySelectorAll(".graphic-value-1");
var graphicNode = document.querySelectorAll(".graphic-1");


if (valueNode != null){
    var value = '';
    for (var i = 0; i < valueNode.length; i++){
        value = valueNode[i].value;
        
        var options = {
            chart: {
                height: 200,
                type: 'radialBar',
            },
            series: [value],
            labels: ['Valor'],
        }
        
            var chart = new ApexCharts(graphicNode[i], options);

            chart.render();
        }
        
    }

