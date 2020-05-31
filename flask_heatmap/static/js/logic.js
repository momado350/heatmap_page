// Creating map object
var myMap = L.map("map", {
  center: [39.0119, -98.4842],
  zoom: 4
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

// Load in geojson data

var geoData = "http://127.0.0.1:5000/api/v1.0/over45percent";


var geojson;

// Grab data with d3
d3.json(geoData, function(data) {
console.log(data);


  // Create a new choropleth layer
  geojson = L.choropleth(data, {

    // Define what  property in the features to use
    //valueProperty: "data_value",
    valueProperty: "obesitypercentage",
    

    // Set color scale
    scale: ["#00FF00", "#0000FF"],

    // Number of breaks in step range
    steps: 10,

    // q for quartile, e for equidistant, k for k-means
    mode: "q",
    style: {
      // Border color
      color: "#fff",
      weight: 1,
      fillOpacity: 0.8
    },

  //   pointToLayer: function (feature, latlng) {
  //     return L.circleMarker(latlng);
  // },
  pointToLayer: function (feature, latlng) {
    return L.circleMarker(latlng);
},
  

    // Binding a pop-up to each layer
    onEachFeature: function(feature, layer) {
      layer.bindPopup("sample size: " + feature.properties.Population2010 + "<br>Percentage of people with Obesity:<br>" +
        "%" + feature.properties.obesitypercentage);
    }
  }).addTo(myMap);

//   // Binding a pop-up to each layer
//   onEachFeature: function(feature, layer) {
//     layer.bindPopup("sample size: " + feature.properties.Population2010 + "<br>Percentage of people with Obesity:<br>" +
//       "%" + feature.properties.obesitypercentage);
//   }
// }).addTo(myMap);

  // Set up the legend
  var legend = L.control({ position: "bottomright" });
  legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");
    var limits = geojson.options.limits;
    var colors = geojson.options.colors;
    var labels = [];

    // Add min & max
    var legendInfo = "<h1>Percentage of people with Obesity</h1>" +
      "<div class=\"labels\">" +
        "<div class=\"min\">" + limits[0] + "</div>" +
        "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
      "</div>";

    div.innerHTML = legendInfo;

    limits.forEach(function(limit, index) {
      labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
    });

    div.innerHTML += "<ul>" + labels.join("") + "</ul>";
    return div;
  };

  // Adding legend to the map
  legend.addTo(myMap);

});
