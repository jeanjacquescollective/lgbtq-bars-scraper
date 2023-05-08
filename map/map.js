fetch('../json/scrapedPages.json')
  .then((response) => response.json())
  .then((json) => createMap(json));

const createMap = (jsonData) => {
  // Create a Leaflet map centered at a default location
  let map = L.map('map').setView([51.054988, 3.724662], 13);

  // Add a tile layer to the map
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18,
  }).addTo(map);
  let lgbtqMarker = L.icon({
    iconUrl: 'marker.png',
    // shadowUrl: 'leaf-shadow.png',

    iconSize:     [38, 95], // size of the icon
    // shadowSize:   [50, 64], // size of the shadow
    // iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    // shadowAnchor: [4, 62],  // the same for the shadow
    // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});
  // Loop through the JSON data and add markers to the map
  for (let place in jsonData) {
    let marker = null;
    if(jsonData[place].lgtbq == true){
      marker = L.marker([
        jsonData[place].metaData.coordinates.latitude,
        jsonData[place].metaData.coordinates.longitude,
      ], {icon: lgbtqMarker}).addTo(map);
    }else{
      marker = L.marker([
        jsonData[place].metaData.coordinates.latitude,
        jsonData[place].metaData.coordinates.longitude,
      ]).addTo(map);
    }
    message = '';
    if (jsonData[place].lgtbq == true) {
      message = 'LGBTQ+ Friendly';
    } else {
      message = 'Not LGBTQ+ Friendly';
    }
    marker.bindPopup(
      '<b>' +
        jsonData[place].metaData.title +
        '</b><br>' +
        jsonData[place].metaData.address +
        '<br><a href="' +
        jsonData[place].metaData.url +
        '" target="_blank">Website</a><br>' +
        message
    );
  }
};
