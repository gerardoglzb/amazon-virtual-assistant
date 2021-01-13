function showLoadingSpinner(button, spinner) {
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