$(document).ready(function() {
	$('form').on('submit', function(e) {
		e.preventDefault();
		// This works as long as there's only one button and loading spinner.
		var b = $(".btn").first();
		var s = $(".loading-spinner").first();
		showLoadingSpinner(b, s);
		$.ajax({
			data: $('form').serialize(),
			type: 'POST',
			url: add_product_url,
			timeout: 10000,
            success: function(data) {
            	if (data.error) {
        			for (error in data.error) {
        				$('#' + error + '-input').addClass('is-invalid');
        				var error_span = document.createElement('span');
        				error_span.innerText = data.error[error];
        				$('#errors-' + error).append(error_span);
        			}
            	} else {
            		check_job_status(data.location);
            	}
            },
            error: function(xhr, status, error) {
            	// var errorMessage = xhr.status + ': ' + xhr.statusText
            	addFlashAlert("An error has occurred. Please try again later.", 'danger');
            	hideLoadingSpinner(b, s);
            }
		});
	});
});

function check_job_status(status_url) {
	console.log("checking...");
	$.getJSON(status_url, function(data) {
		console.log(data.status);
	    switch (data.status) {
			case "unknown":
			case "failed":
			case "amazon":
			case "invalid":
				var b = $(".btn").first();
				var s = $(".loading-spinner").first();
				hideLoadingSpinner(b, s);
				addFlashAlert(data.msg, 'danger');
				break;
			case "finished":
				window.location.replace(home_url);
	          	break;
			default:
				setTimeout(function() {
					check_job_status(status_url);
				}, 1000);
    	}
    });
}