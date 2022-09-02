$(document).ready(function(){

    $('#sensor-value').on('change', function(){

        $.ajax({
            type: 'GET',
            url:    'ajax/sensor/',
            data: { sensor : $('#sensor-value').val()},
            success : function(response){
                console.log($('#sensor-value').val())

                $('#value-current-sensor').empty()
                $('#datetime').empty()

                var value = document.getElementById('value-current-sensor')
                value.value = response.sensor[0].value

                var valueData = response.sensor[0].datetime.split('T')
                var data = valueData[0]
                var hora = valueData[1]

                var datetime = document.getElementById('datetime')
                datetime.innerHTML = `${data.split('-').reverse().join('/')} - ${hora.split('Z')[0]}` 
            },
            error: function(response){
                var value = document.getElementById('value-current-sensor')
                value.value =  'Valor Atual'

                var datetime = document.getElementById('datetime')
                datetime.setAttribute('type','datetime-local')
                datetime.value = ''
            }
        })

    })

})