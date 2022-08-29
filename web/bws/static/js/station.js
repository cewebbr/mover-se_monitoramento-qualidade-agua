function sensorValueData() {
    
    var sensor_key = document.getElementById('sensor-value').value
    var station_id = parseInt(document.getElementById('id-station').value)
    
    var button = document.getElementById('btn-sensor')

    if (sensor_key === '------- ------') {
        button.setAttribute('href',`#`)
    }
    else {
        
        button.setAttribute('href',`/station/${station_id}/sensor/${sensor_key}/`)
    }
    
}
