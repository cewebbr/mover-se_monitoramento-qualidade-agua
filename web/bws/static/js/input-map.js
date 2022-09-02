function addMapPicker() {
    var mapCenter = [22, 87];
    var map = L.map('map').setView([-10.658470336291018, -50.70587977228521], 4);
    L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=h9QcRHycQ6mEJBkYlPyW', {
                 attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
                 maxZoom: 20,
                 tileSize: 512,
                 zoomOffset: -1
             }).addTo(map);
     var marker = L.marker(mapCenter).addTo(map);
     function updateMarker(lat, lng) {
         marker
             .setLatLng([lat, lng])
             .bindPopup("Sua localização:  " + marker.getLatLng().toString())
             .openPopup();
         return false;
     };
     
     map.on('click', function(e) {
         $('#latInput').val(e.latlng.lat);
         $('#lngInput').val(e.latlng.lng);
         updateMarker(e.latlng.lat, e.latlng.lng);
     });
          
     var updateMarkerByInputs = function() {
         return updateMarker( $('#latInput').val() , $('#lngInput').val());
     }
     
     $('#latInput').on('input', updateMarkerByInputs);
     $('#lngInput').on('input', updateMarkerByInputs);
 }
 
 $(document).ready(function() {
     addMapPicker();
 });