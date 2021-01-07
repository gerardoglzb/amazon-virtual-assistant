from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user
from app.models import User, Product

from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def home():
	if current_user.is_authenticated:
		page = request.args.get('page', 1, type=int)
		user = User.query.filter_by(username=current_user.username).first_or_404()
		products = Product.query.filter_by(author=user).order_by(Product.id.desc()).paginate(page=page, per_page=5)
		return render_template('index.html', products=products)
	return redirect(url_for('users.register'))