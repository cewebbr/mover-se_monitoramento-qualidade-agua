$(document).ready(function(){

    $('#select-station').on('change', function(){

        $.ajax({
            type : 'GET',
            url : 'ajax/sensor/',
            data : { station : $('#select-station').val()},
            success : function(response){

                $('#sensor-value').empty()

                    var selectNode = document.getElementById('sensor-value')
                    var defaultNode = document.createElement('option')
                    defaultNode.innerHTML = 'Escolher sensor'
                    selectNode.append(defaultNode)
                    
                    for (var key in response.sensores){                        
                        var optionNode = document.createElement('option')   
                        optionNode.innerHTML = response.sensores[key]
                        optionNode.value = key
                        selectNode.append(optionNode)
                    }

            },
            error: function(response){
                $('#sensor-value').empty()
                
                var selectNode = document.getElementById('sensor-value')
                var defaultNode = document.createElement('option')
                defaultNode.innerHTML = 'Escolher sensor'
                selectNode.append(defaultNode)
            }
    
         });

    })

})