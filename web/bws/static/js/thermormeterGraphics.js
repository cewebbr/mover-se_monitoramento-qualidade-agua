var valueNode = document.querySelectorAll(".graphic-value-2");
var graphicNode = document.querySelectorAll(".graphic-2");
var currentNode = document.querySelectorAll(".current-value-2");


if (valueNode != null){
  var value = '';
  
  for (var i = 0; i < valueNode.length; i++){
      value = valueNode[i].innerHTML;
      var color = currentNode[i].value <= 40 ? "#008ee4": "red";

      $(graphicNode[i]).tempGauge({

        borderColor: color,
        borderWidth: 2,
        defaultTemp: 26,
        fillColor: color,
        showLabel: true,
        showScale: false,
        labelSize: 20,
        maxTemp: 45,
        minTemp: 0,
        padding: 5,
        width:100,
        replaceHtml: true
      });
    }
}
