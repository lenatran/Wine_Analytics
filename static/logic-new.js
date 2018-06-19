// initializes map with baselayer. Returns map instance with baselayer
function initMap(){   
    
    var mybaseTileLayer = baseLayer();
    myMap = L.map('map', {
        center: [37.0902, -95.7129],
        zoom: 4,
        layers: [mybaseTileLayer]
    });
    //myMap.fitWorld();
    return myMap;   
}

//function that prepares a baselayer for the map.
function baseLayer(){
    // create a tile layer that will be the background of our map.
    var mapbox = 'https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?' + 'access_token=pk.eyJ1IjoiamRrb3JhIiwiYSI6ImNqaWc4ZDc0djBpajczb3QxMm91NmNnY28ifQ.FgOYmoVC85ZTAaeViPiTDQ';
    
    //create a tile layer
    var mybaseLayer = L.tileLayer(mapbox);
    // create a baseMaps object to hold the baselayer
      var baseMaps = {
        "Map": baseLayer
      };
    return mybaseLayer;
}

//function that takes data from getData and draws markers. returns a marker layer group.
function createMarkers(wineData, regData){ 
    wlayer = new L.LayerGroup();
    //console.log(wineData)
    console.log(regData);
    console.log(wineData[0].region);
    var wineReg = wineData[0].region;
    // pull the winery coordinates from the regData
    var coords = regData[0].coordinates;
    //console.log(coords.length);
    //initialize an array to hold the quake markers
    var wMarkers = [];
    
    //loop thru the wineData regions array
    for (var i=0; i < wineReg.length; i++){
        //for each region in regionData 
        for (var j=0; j<coords.length; j++){
            //if coords are available
            if (coords[j]){
                //console.log(coords[j]);
                //find the region co-ordinates for the wineData
                if (wineData[0].region[i] == regData[0].region[j]){
                    //get the co-ordiantes to a variable
                    var wineryLocation =JSON.parse(coords[j]);
                    // set the markerOptions
                    var markerOptions = {
                        fillColor: "#4B0082",
                        color: "white",
                        weight:1,
                        opacity: 1,
                        fillOpacity: 0.5,
                        radius: wineData[0].points[i]*800
                    };
                }//end of IF loop checking wineData.region with regionData 
                
            } //end of IF loop verifying coords exist      
    }//end of regionData FOR loop
        console.log(wineryLocation);
    // for each winery location, create a marker and bind a pop with properties
        var wineryMarker = L.circle([wineryLocation[0], wineryLocation[1]], markerOptions).bindPopup("<h5> Name: "+wineData[0].title[i] + "</h5> <br> <h5> Rating : " + wineData[0].points[i] + "</h5> <br> <h5> Winery : " + wineData[0].winery[i] + "</h5>");
        //add marker to wlayer
        wineryMarker.addTo(wlayer);
        wMarkers.push(wineryMarker);
}
    //wMarkers.addTo(wlayer);
    return wlayer; 
}

function addMarkers(wineData, regData){
    var myMap = initMap();
    var myLayer = createMarkers(wineData, regData);
    //console.log(myLayer);
    myLayer.addTo(myMap);
}


function updateMarkers(wineData, regData){
    var newLayer = createMarkers(wineData, regData);
    myMap.eachLayer(function(layer){
        console.log(layer[1]);
        myMap.removeLayer(layer);
    });
    var mybaseTileLayer = baseLayer();
    mybaseTileLayer.addTo(myMap);
    newLayer.addTo(myMap);
    
}
    