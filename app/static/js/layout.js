function showLoadingSpinner(button, spinner) {
	console.log("showing spinner");
	button.css('display', 'none');
	spinner.css('display', 'inline-block');
}

function hideLoadingSpinner(button, spinner) {
	spinner.css('display', 'none');
	button.css('display', 'inline-block');
}

function addFlashAlert(message, category) {
	var alert_element = $('<div>', {'class': 'alert alert-' + category + ' fade show', text: message});
	$('#main-container').prepend(alert_element);
	console.log("aqhii");
	console.log(alert_element);
	deleteFlashAlert(alert_element);
}

var validate_price = function(e) {
	var t = e.value;
	e.value = (t.indexOf(".") >= 0) ? (t.substr(0, t.indexOf(".")) + t.substr(t.indexOf("."), 3)) : t;
}

function deleteFlashAlert(flashAlert) {
	setTimeout(function() {
		console.log("aqui vamos");
		console.log(flashAlert);
		flashAlert.alert('close');
	}, 10000);
}

$(document).ready(function() {
	$('.alert').each(function() {
		deleteFlashAlert($(this));
		console.log()
	});
});