from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError


class ProductForm(FlaskForm):
	link = StringField('Link', validators=[DataRequired(), Length(min=2, max=1000)])
	optimal_price = FloatField('OptimalPrice', validators=[DataRequired()])
	submit = SubmitField('Add Product')

	def validate_link(form, field):
		amazon_sites = (
			'https://www.amazon.co.uk/',
			'https://www.amazon.com/',
			'https://www.amazon.ca/',
			'https://www.amazon.com.au/'
		)

		if not field.data.startswith(amazon_sites):
			raise ValidationError("This website is not allowed.")
