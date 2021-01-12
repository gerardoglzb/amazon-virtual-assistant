from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
	code = "404 ERROR"
	msg = "Page not found. Make sure you got the right address."
	return render_template('errors/errors_template.html', code=code, msg=msg), 404


@errors.app_errorhandler(403)
def error_403(error):
	code = "403 ERROR"
	msg = "You do not have permission to access this page."
	return render_template('errors/errors_template.html', code=code, msg=msg), 403


@errors.app_errorhandler(500)
def error_500(error):
	code = "500 ERROR"
	msg = "We're having some trouble in our end. Sorry."
	return render_template('errors/errors_template.html', code=code), 500
