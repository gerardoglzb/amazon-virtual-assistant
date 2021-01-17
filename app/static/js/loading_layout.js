$(document).ready(function() {
	var b = $(".btn").first();
	console.log(b);
	var s = $(".loading-spinner").first();
	console.log(s);
	$('form').on('submit', function(e) {
		console.log("detectedddd");
		// This works as long as there's only one button and loading spinner.
		var b = $(".btn").first();
		var s = $(".loading-spinner").first();
		showLoadingSpinner(b, s);
	});
});