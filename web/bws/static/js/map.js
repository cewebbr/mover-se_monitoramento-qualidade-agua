$(document).ready(function(){

    $.ajax({
        type : 'GET',
        url : 'map/',
        success : function(response){

            var map = L.map('mapid').setView([-10.658470336291018, -50.70587977228521], 5);
    
            var markers = L.markerClusterGroup({
                spiderfyOnMaxZoom: false,
                showCoverageOnHover: false,
                zoomToBoundsOnClick: true
            });

            L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=h9QcRHycQ6mEJBkYlPyW', {
                attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
                maxZoom: 18,
                tileSize: 512,
                zoomOffset: -1
            }).addTo(map);


            for(var i = 0; i < response.map.length; i++){
                for(var j = 0; j < response.map[i].length; j++){
                    
                    //pegando imagem para criar o popup
                    var icon_pointer = L.icon({
                        iconUrl : './static/img/icon/' + response.map[i][j].custom_icon,
                        iconSize: [50,50],
                        iconAnchor: [22,94],
                        popuoAnchor: [0, -15]
                    });

                    var marker = L.marker([response.map[i][j].lat, response.map[i][j].lon], {icon : icon_pointer});
                    
                    marker.bindPopup(
                        '<h3 style ="color:orange"> <strong>' + response.map[i][j].titulo + '<strong> </h3>' +  
                        '<p>Informações</p>' + 
                        '<p>latitude: ' + response.map[i][j].lat + '</p> <p>longitude: ' + response.map[i][j].lon + '</p>' + 
                        '<a href="' + response.map[i][j].url + response.map[i][j].id + '"> ver mais </a>');
                    
                    markers.addLayer(marker);
                    map.addLayer(markers);

                }
                
            }

        }
    });
})