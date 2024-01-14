$(document).ready(function() {
	// Dictionary to store checked amenities
	let checkedAmenities = {};

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
});
