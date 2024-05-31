var map, marker, routeControl;

function initializeMap(latitude, longitude) {
    map = L.map('map').setView([latitude, longitude], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // User current location marker
    marker = L.marker([latitude, longitude]).addTo(map);
    marker.bindPopup("<b>You are here!</b>").openPopup();

    document.querySelector('.currentBtn').addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var lat = position.coords.latitude;
                var lon = position.coords.longitude;
                map.setView([lat, lon], 13);
                marker.setLatLng([lat, lon]);
                marker.bindPopup("<b>You are here!</b>").openPopup();
            });
        }
    });

    document.querySelector('.search__button').addEventListener('click', function() {
        var query = document.querySelector('.search__input').value;
        if (query) {
            var viewbox = `${longitude - 0.05},${latitude - 0.05},${longitude + 0.05},${latitude + 0.05}`;
            var bounded = 1;

            fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}&viewbox=${viewbox}&bounded=${bounded}`)
                .then(response => response.json())
                .then(data => {
                    var resultsList = document.querySelector('.search__result');
                    resultsList.innerHTML = '';

                    if (data.length > 0) {
                        data.forEach(location => {
                            var listItem = document.createElement('li');
                            listItem.textContent = location.display_name;
                            listItem.addEventListener('click', function() {
                                var lat = location.lat;
                                var lon = location.lon;
                                map.setView([lat, lon], 13);
                                marker.setLatLng([lat, lon]);
                                marker.bindPopup(`<b>${location.display_name}</b><br><button class="directionBtn">Directions</button>`).openPopup();

                                document.querySelector('.directionBtn').addEventListener('click', function() {
                                    if (routeControl) {
                                        map.removeControl(routeControl);
                                    }
                                    routeControl = L.Routing.control({
                                        waypoints: [
                                            L.latLng(latitude, longitude),
                                            L.latLng(lat, lon)
                                        ],
                                        routeWhileDragging: true
                                    }).addTo(map);
                                });
                                resultsList.innerHTML = '';
                            });
                            resultsList.appendChild(listItem);
                        });
                    } else {
                        resultsList.innerHTML = '<li>No locations found.</li>';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });

    map.on('click', function() {
        document.querySelector('.search__result').innerHTML = '';
    });

    // function handleKeyPress(event) {
    //     if (event.key === "Enter") {
    //         document.querySelector('.search__result').innerHTML = '';
    //     }
    // }

    // resultsList.addEventListener("keypress", handleKeyPress);

    // Continuously update user's location
    setInterval(function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    var lat = position.coords.latitude;
                    var lon = position.coords.longitude;
                    marker.setLatLng([lat, lon]);
                    marker.bindPopup("<b>You are here!</b>").openPopup();
                },
                function(error) {
                    console.error("Error retrieving location: ", error);
                }
            );
        } else {
            console.error("Geolocation not available");
        }
    }, 10000); // Update every 10 secs.
}

// Check if geolocation is available
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            initializeMap(latitude, longitude);
        },
        function(error) {
            console.error("Error retrieving location: ", error);
            initializeMap(51.505, -0.09);
        }
    );
} else {
    console.error("Geolocation not available");
    initializeMap(51.505, -0.09);
}
