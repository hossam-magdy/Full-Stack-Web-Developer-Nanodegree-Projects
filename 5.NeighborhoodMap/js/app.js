
var URI_dataJSON = './data.json';

var ViewModel = function(){
    var self = this;

    self.markers = [];
    self.infowindow = new google.maps.InfoWindow();

    var locations = [];

    // Fill the local var locations
    // Creating filtered.subscribe for each element
    for (var i=0;i<initLocations.length;i++) {
        initLocations[i].filtered = ko.observable(1);
        initLocations[i].thirdPartyContent = '';
        //var location = ko.observable(initLocations[i]);
        //locations.push(location);
        locations[i] = ko.observable(initLocations[i]);
        locations[i].subscribe(self.locationChangedHandler);
    }

    self.locations = ko.observableArray(locations);

    // At changing locations observable, reset the markers
    self.locations.subscribe(function (newLocations) {
        clearAllMarkersMap(self.markers);
        self.markers = [];
        var bounds = new google.maps.LatLngBounds();
        for (var i=0;i<newLocations.length;i++) {
            if(newLocations[i]().filtered()) {
                bounds.extend(newLocations[i]().latlng);
            }
            self.markers[i] = new google.maps.Marker({
                map: (newLocations[i]().filtered() ? map : null),
                title: newLocations[i]().name,
                position: newLocations[i]().latlng,
                animation: google.maps.Animation.DROP,
            });

            // Re-update the latlng with the accurate/approximated one of the placed marker
            // Because latLng is used to search for location in locations obsArray
            var latLng = self.markers[i].getPosition();
            newLocations[i]().latlng = {lat: latLng.lat(), lng: latLng.lng()};

            self.markers[i].addListener('click', self.clickLocationByGoogleEvent);
        }
        if(bounds.getCenter().lat()!==0 && bounds.getCenter().lng()!==0)
            map.fitBounds(bounds);
            google.maps.event.addDomListener(window, 'resize', function() {
                map.fitBounds(bounds);
            });
    });

    // Create the observable "filterVal"
    self.filterVal = ko.observable('');
    self.filterVal.subscribe(function (newVal) {
        var query = newVal.toLowerCase().trim();
        var locs = self.locations().slice();
        for (var i=0;i<self.locations().length;i++) {
            if(query==='' || self.locations()[i]().name.toLowerCase().indexOf(query) >= 0){
                self.locations()[i]().filtered(1);
            } else {
                self.locations()[i]().filtered(0);
            }
            self.locationChangedHandler(self.locations()[i]());
        }
    });

    // Create the function "locationChangedHandler"
    self.locationChangedHandler = function(newLocation){
        var index = self.indexOfLocation(newLocation);
        self.markers[index].setVisible(newLocation.filtered() ? true : false);
        self.hideInfoWindow();
    };
    
    // Create the function "hideInfoWindow"
    self.hideInfoWindow = function(){
        self.infowindow.close();
    };

    // Create the function "showInfoWindowByIndex"
    self.showInfoWindowByIndex = function(index){
        var location = self.locations()[index]();
        var marker = self.markers[index];
        if(!location.thirdPartyContent) {
            loadThirdPartyContent(index);
            self.infowindow.setContent('<div id="infoWindow" title="' + location.name + '">' + location.name + '<br>Loading 3rd-party data ...' + '</div>');
        } else {
            self.infowindow.setContent('<div id="infoWindow" title="' + location.name + '">' + location.thirdPartyContent + '</div>');
        }
        self.infowindow.open(map, marker);
    };

    // Create the function "indexOfLocation"
    self.indexOfLocation = function(location){
        var index = -1;
        for (var i=0;i<self.locations().length;i++) {
            if(self.locations()[i]().latlng.lat == location.latlng.lat && 
                self.locations()[i]().latlng.lng == location.latlng.lng){
                return i;
            }
        }
    };

    // Create the function "clickLocation"
    self.clickLocation = function(location){
        var index = self.indexOfLocation(location);
        self.clickLocationByIndex(index);
    };

    // Create the function "clickLocationByGoogleEvent"
    self.clickLocationByGoogleEvent = function(e){
        var index = self.indexOfLocation({latlng: {lat: e.latLng.lat(), lng: e.latLng.lng()}});
        self.clickLocationByIndex(index);
    };

    // Create the function "clickLocationByIndex"
    self.clickLocationByIndex = function(index){
        var marker = self.markers[index];
        bounceMarker(marker);
        self.showInfoWindowByIndex(index);
    };

    // Create the function "saveThirdPartyContent"
    self.saveThirdPartyContent = function(index, content){
        var newLocation = self.locations()[index]();
        newLocation.thirdPartyContent = content;
        self.locations.replace(self.locations()[index](), newLocation);
        self.showInfoWindowByIndex(index);
    };

    // initialize function to call subscribers/listeners of "locations" observable at page load
    self.initialize = function(){
        self.locations.valueHasMutated();
    };

};

function loadThirdPartyContent(index){
    var url = 'https://api.foursquare.com/v2/venues/search' +
                '?client_id=0UK5OMAR5R4XHPCONM3NE1KYGYV4A1M25UI32FZTY2GTWDRD' +
                '&client_secret=JNSRTD2VV12OGADYVU2JKP3SNO253DHIZ2JW0V411BCVJA4K' +
                '&ll=' + appViewModel.locations()[index]().latlng.lat + ',' + appViewModel.locations()[index]().latlng.lng +
                '&query=' + appViewModel.locations()[index]().name +
                '&v=20170610&m=foursquare';
    var content = '';
    $.getJSON(url).done(function(response1) {
        var url = 'https://api.foursquare.com/v2/venues/' +
                    response1.response.venues[0].id +
                    '?client_id=0UK5OMAR5R4XHPCONM3NE1KYGYV4A1M25UI32FZTY2GTWDRD' +
                    '&client_secret=JNSRTD2VV12OGADYVU2JKP3SNO253DHIZ2JW0V411BCVJA4K' +
                    '&v=20170610&m=foursquare';
        $.getJSON(url).done(function(response2) {
            if(response2.response.venue.shortUrl) content += '<a href=" ' + response2.response.venue.shortUrl + '" target="_blank">';
            if(response2.response.venue.name) content += '' + response2.response.venue.name;
            if(response2.response.venue.shortUrl) content += '</a>';
            //content += '<br>Address: ' + response2.response.venue.location.formattedAddress.join(', ');
            //if(response2.response.venue.stats.visitsCount) content += '<br>Visits count: ' + response2.response.venue.stats.visitsCount;
            if(response2.response.venue.rating) content += '<br>Rating: ' + response2.response.venue.rating;
            if(response2.response.venue.bestPhoto) content += '<br><img src=" ' + response2.response.venue.bestPhoto.prefix + '150x150' + response2.response.venue.bestPhoto.suffix + '">';
            appViewModel.saveThirdPartyContent(index, content);
        }).fail(function(jqXHR, status) {
            appViewModel.hideInfoWindow();
            alert("Requesting third-party data failed: " + status);
        });
    }).fail(function(jqXHR, status) {
        appViewModel.hideInfoWindow();
        alert("Requesting third-party data failed: " + status);
    });
}

function initMap() {
    map = new google.maps.Map($('.map')[0], {
        zoom: 11,
        center: initLocations[0].latlng,
        mapTypeControl: false
    });
}

function clearAllMarkersMap(markers) {
    for (var i=0;i<markers.length;i++) {
        markers[i].setVisible(false);
    }
}

function bounceMarker(marker) {
    marker.setAnimation(google.maps.Animation.BOUNCE);
    setTimeout(function(){ marker.setAnimation(null); }, 1400);
}

function initAll() {
    // http://www.jsoneditoronline.org/
    $.getJSON(URI_dataJSON)
        .done(function(response) {
            initLocations = response;
        })
        .fail(function(jqXHR, status) {
            alert("Requesting initial locations failed: " + status + "\nTrivial data will be used instead.");
            initLocations = [
                    {
                        name: 'x McDonald\'s (Shobra)',
                        latlng: {lat: 30.0774687, lng: 31.2457931}
                    },
                    {
                        name: 'x Pizza Hut (Giza)',
                        latlng: {lat: 30.0246363, lng: 31.21673}
                    },
                    {
                        name: 'x Pizza Hut (AlHaram)',
                        latlng: {lat: 29.9961615, lng: 31.1655521}
                    },
                    {
                        name: 'x AUC (American University in Cairo)',
                        latlng: {lat: 30.043021, lng: 31.2366105}
                    },
                    {
                        name: 'x GUC (German University in Cairo)',
                        latlng: {lat: 29.9866117, lng: 31.4415113}
                    },
                    {
                        name: 'x Smart Village',
                        latlng: {lat: 30.0731306, lng: 31.0180683}
                    },
                    {
                        name: 'x Cairo University',
                        latlng: {lat: 30.0273275, lng: 31.2086334}
                    },
                    {
                        name: 'x Cairo International Airport',
                        latlng: {lat: 30.1188025, lng: 31.4108734}
                    },
                    {
                        name: 'x Giza Pyramids',
                        latlng: {lat: 29.9790858, lng: 31.1344862}
                    },
                    {
                        name: 'x Cairo Tower',
                        latlng: {lat: 30.0458988, lng: 31.2243256}
                    },
                ];
        })
        .always(function() {
            initMap();

            appViewModel = new ViewModel();

            ko.applyBindings( appViewModel );

            appViewModel.initialize();
        })
    ;
}

function errorInitAll() {
    alert("Error loading Google Maps API library");
}

