from flask import render_template, request, url_for, Blueprint
from flask_login import current_user
from app.models import User, Product
from app.products.forms import ProductForm

from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def home():
	if current_user.is_authenticated:
		# page = request.args.get('page', 1, type=int)
		user = User.query.filter_by(username=current_user.username).first_or_404()
		# products = Product.query.filter_by(author=user).order_by(Product.id.desc()).paginate(page=page, per_page=9)
		products = Product.query.filter_by(author=user).order_by(Product.id.desc())
		form = ProductForm()
		return render_template('index.html', products=products, form=form)
	return render_template('landing_page.html')


@main.route('/about')
def about():
	return render_template('about.html', title="About", active=1)


@main.route('/testing')
def testing():
	return render_template('testing.html')
