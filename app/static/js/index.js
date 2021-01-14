// TODO: On document ready

$('#deleteModal').on('show.bs.modal', function(event) {
	var button = $(event.relatedTarget);
	var url = button.data('url');
	var price = button.data('price');
	var name = button.data('name');
	modal = $(this);
	modal.find('.modal-footer form').attr('action', url);
	modal.find('.modal-body .product-name').text(name);
});

var url = "";

$('#editModal').on('show.bs.modal', function(event) {
	var button = $(event.relatedTarget);
	var current_price = button.data('current-price');
	var optimal_price = button.data('optimal-price');
	var currency_code = button.data('currency-code');
	url = button.data('url');
	$('#currentPrice').val(current_price + " " + currency_code);
	$('#optimalPrice').val(optimal_price + " " + currency_code);
	// $('#newPrice').val(parseFloat(optimal_price));
	modal = $(this);
	modal.find('.modal-content form').attr('action', url);
});

$(document).ready(function() {
	$('#edit-form').on('submit', function(e) {
		e.preventDefault();
		var b = $("#edit-btn");
		var s = $("#edit-spinner");
		showLoadingSpinner(b, s);
		$.ajax({
			data: $('#edit-form').serialize(),
			type: 'POST',
			url: url,
            success: function(data) {
            	if (data.error) {
            		console.log(data.error);
            		$('#optimal-price-input').addClass('is-invalid');
            		var error_span = document.createElement('span');
            		error_span.innerText = "The price must be a valid amount of money.";
            		$('#invalid-feedback-div').append(error_span);
            	} else {
            		window.location.href = home_url;
            	}
            },
            error: function(xhr, status, error) {
            	// var errorMessage = xhr.status + ': ' + xhr.statusText
            	alert("An error has occurred. Please try again later.");
            	hideLoadingSpinner(b, s);
            }
		});
	});
	$('#delete-form').on('submit', function(e) {
		var b = $("#delete-btn");
		var s = $("#delete-spinner");
		showLoadingSpinner(b, s);
	})
});