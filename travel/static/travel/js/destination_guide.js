// For displaying the maps for each desdtination
document.addEventListener("DOMContentLoaded", function() {
    // Uses the latitude and longitude variables from the template
    var map = L.map('destination-map').setView([latitude, longitude], 12);

    var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: `&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>`
    }).addTo(map);

    var markers = [];

     // Custom icon
    var Icon = new L.Icon({
        iconUrl: 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/map-marker-512.png',
        iconSize: [38, 95],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    // Gets the URL for the attraction_fixture.json from the data attribute
    var attractionUrl = document.getElementById('destination-map').getAttribute('data-attraction-url');

    // Fetches the attraction_fixture.json file
    fetch(attractionUrl)
    .then(response => response.json())
    .then(data => {
        data.forEach(attraction => {
            // Extract name, attraction image, coordinates (lattiude and longitude) and location
            var name = attraction.fields.name;
            var image = attraction.fields.attraction_image;
            var attraction_lat = attraction.fields.latitude;
            var attraction_lng = attraction.fields.longitude;



            // Checks if latitude and longitude are valid
            if(attraction_lat!== undefined && attraction_lng !== undefined) {

                // Prepend static path if needed (ensure your image path is correct)
                var imageUrl = image.startsWith('static') ? `/${image}` : image;
                // A marker is created and an pop-up is binded 
                var marker = L.marker([attraction_lat, attraction_lng], { icon: Icon }).addTo(map);

                var popupContent = `
                <img src="${imageUrl}" width="250" height="144">
                <br>
                <br>
                <strong>${name}</strong>
                `;

                marker.bindPopup(popupContent);

                markers.push(marker);
            } else {
                console.error('Invalid latitude or longitude for:', attraction);
            }
        });
    })
})

// for handling the star rating
document.addEventListener("DOMContentLoaded", function() {
    const stars = document.querySelectorAll(".star-rating .star");
    const ratingInput = document.getElementById("rating-input");

    stars.forEach((star) => {

        star.addEventListener("click", function () {
            const ratingValue = this.getAttribute("data-value");
            ratingInput.value = ratingValue;


            // Update stars based on selection
            stars.forEach((s, index) => {
                if(index < ratingValue) {
                    s.classList.add("selected")
                } else {
                    s.classList.remove("selected")
                }

            });
        })
    })
})