var map = L.map('destination-list-map').setView([0, 0], 2);

var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: `&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`
}).addTo(map);

var markers = [];

// Fetches the destination_fixture.json file
fetch(`static/travel/fixtures/destination_fixture.json`)
    .then(response => response.json())
    .then(data => {
        data.forEach(destination => {
            // Extract name, destination image, coordinates (lattiude and longitude) and location
            var name = destination.fields.name;
            var image = destination.fields.destination_image;
            var lat = destination.fields.latitude;
            var lng = destination.fields.longitude;
            var location = destination.fields.location;


            // Checks if latitude and longitude are valid
            if(lat !== undefined && lng !== undefined) {
                // A marker is created and an pop-up is binded
                var marker = L.marker([lat, lng]).addTo(map);

                var popupContent = `
                <img src="${image}" width="250" height="144">
                <br>
                <br>
                <strong>${name}</strong>
                <br>
                <br>
                ${location}`;

                marker.bindPopup(popupContent);

                markers.push(marker);
            } else {
                console.error('Invalid latitude or longitude for:', destination);
            }
        });
    })