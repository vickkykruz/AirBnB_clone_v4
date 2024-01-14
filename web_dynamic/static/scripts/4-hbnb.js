$(document).ready(function() {
	// Dictionary to store checked amenities
	let checkedAmenities = {};
	const apiUrl = "http://0.0.0.0:5001/api/v1/status/";
	const apiPlaces = "http://0.0.0.0:5001/api/v1/places_search/";

	// New code to handle filter button click
  	const filterButton = document.getElementById('filter_btn');

	// Function to update the h4 tag with the list of checked amenities
	function updateAmenitiesList() {
		let checkedAmenitiesList = Object.values(checkedAmenities).join(', ');
		$('.amenities h4').text('Amenities: ' + checkedAmenitiesList);
	}

	// Listen for changes on each input checkbox tag
	$('.amenities ul li input[type="checkbox"]').change(function() {
		let amenityId = $(this).closest('li').data('id');
		let amenityName = $(this).closest('li').data('name');

		if ($(this).is(':checked')) {
			// If checkbox is checked, store the Amenity ID in the dictionary
			checkedAmenities[amenityId] = amenityName;
		} else {
			// If checkbox is unchecked, remove the Amenity ID from the dictionary
			delete checkedAmenities[amenityId];
		}

		// Update the h4 tag with the list of checked amenities
		updateAmenitiesList();
	});

	filterButton.addEventListener('click', function () {
		// Get the list of checked amenities
    		const checkedAmenitiesInput = document.querySelectorAll('.amenities input:checked');
    		const amenityIds = Array.from(checkedAmenitiesInput).map(amenity => amenity.getAttribute('data-id'));

		// Fetch the data from 'http://0.0.0.0:5001/api/v1/status'
		fetch(apiUrl).then(response => response.json()).then(data => {
			const apiStatusDiv = document.getElementById('api_status');

			if (data.status === 'OK') {
				apiStatusDiv.classList.add('available');
			} else {
				apiStatusDiv.classList.remove('available');
			}
		}).catch(error => {
			console.error('Error fetching API status:', error);
		});

		// Fetch the place search
		fetch(apiPlaces, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({amenities: amenityIds})
		}).then(response => response.json())
		.then(places => {
			const placeSection = document.querySelector('.places');
		
			// Run the loop
			places.forEach(place => {
				const article = document.createElement('article');
				article.innerHTML = `
				<div class="title_box">
            				<h2>${{ place.name }}</h2>
            				<div class="price_by_night">$${ place.price_by_night }</div>
          			</div>
          			<div class="information">
            				<div class="max_guest">${ place.max_guest } Guest{% if place.max_guest != 1 %}s{% endif %}</div>
            				<div class="number_rooms">${ place.number_rooms } Bedroom{% if place.number_rooms != 1 %}s{% endif %}</div>  		<div class="number_bathrooms">${ place.number_bathrooms } Bathroom{% if place.number_bathrooms != 1 %}s{% endif %}</div>
          			</div>
          			<div class="user">
            				<b>Owner:</b> ${ place.user.first_name } ${ place.user.last_name }
          			</div>
          			<div class="description">
            				${ place.description | safe }
          			</div>
				`;
				placesSection.appendChild(article);
			});
		}) .catch(error => {
      			console.error('Error fetching places:', error);
    		});
	});
});
