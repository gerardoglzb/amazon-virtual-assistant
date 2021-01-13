$(document).ready(function() {
	$('form').on('submit', function(e) {
		// This works as long as there's only one button and loading spinner.
		var b = $(".btn").first();
		var s = $(".loading-spinner").first();
		showLoadingSpinner(b, s);
	});
});