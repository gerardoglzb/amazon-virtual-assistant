function showLoadingSpinner(button, spinner) {
	console.log("showing spinner");
	button.css('display', 'none');
	spinner.css('display', 'inline-block');
}

function hideLoadingSpinner(button, spinner) {
	spinner.css('display', 'none');
	button.css('display', 'inline-block');
}

var validate_price = function(e) {
	var t = e.value;
	e.value = (t.indexOf(".") >= 0) ? (t.substr(0, t.indexOf(".")) + t.substr(t.indexOf("."), 3)) : t;
}

function deleteFlashAlerts() {
	setTimeout(function() {
		$('.alert').alert('close');
	}, 10000);
}

$(document).ready(function() {
	deleteFlashAlerts();
});