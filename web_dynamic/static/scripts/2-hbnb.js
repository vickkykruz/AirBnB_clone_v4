$(document).ready(function() {
	// Dictionary to store checked amenities
	let checkedAmenities = {};
	const apiUrl = "http://0.0.0.0:5001/api/v1/status/";

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
});
