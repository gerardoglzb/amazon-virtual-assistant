from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
	link = StringField('Link', validators=[DataRequired(), Length(min=2, max=1000)])
	optimal_price = FloatField('OptimalPrice', validators=[DataRequired()])
	submit = SubmitField('Add Product')
