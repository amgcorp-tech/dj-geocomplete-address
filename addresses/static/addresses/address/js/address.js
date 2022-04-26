$(function () {
	$('input.address').each(function () {
		var self = $(this);
		var cmps = $('#' + self.attr('name') + '_components');
		var fmtd = $('input[name="' + self.attr('name') + '_formatted"]');
		self.geocomplete({
			details: cmps,
			detailsAttribute: 'data-geo'
		}).change(function () {
			if (self.val() != fmtd.val()) {
				var cmp_names = [
					'country',
					'country_code',
					'locality',
					'postal_code',
					'postal_town',
					'route',
					'street_number',
					'state',
					'state_code',
					'formatted',
					'latitude',
					'longitude',
				];

				for (var ii = 0; ii < cmp_names.length; ++ii) {
					$('input[name="' + self.attr('name') + '_' + cmp_names[ii] + '"]').val('');
				}
			}
		});
	});
});



/*
$(function () {
	$('input.address').each(function () {
		var self = $(this);
		var cmps = $('#' + self.attr('name') + '_components');
		var fmtd = $('input[name="' + self.attr('name') + '_formatted"]');
		self.geocomplete({
			details: cmps,
			detailsScope: '.location',
			detailsAttribute: 'data-geo'
		/!*}).change(function () {
			if (self.val() != fmtd.val()) {
				var cmp_names = [
					'country',
					'country_code',
					'locality',
					'postal_code',
					'postal_town',
					'route',
					'street_number',
					'state',
					'state_code',
					'formatted',
					'latitude',
					'longitude',
					'url',
				];

				for (var ii = 0; ii < cmp_names.length; ++ii) {
					$('input[name="' + self.attr('name') + '_' + cmp_names[ii] + '"]').val('');
				}
			}*!/
		}).bind("geocode:result", function(event, result){
            console.log("Result: " + result.formatted_address);
            $(this).parents(".location").find(".address").val(result.formatted_address);
          })
          .bind("geocode:error", function(event, status){
            console.log("ERROR: " + status);
          })
          .bind("geocode:multiple", function(event, results){
            console.log("Multiple: " + results.length + " results found");
          });
	});
});*/
