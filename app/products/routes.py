from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Product
from app.products.forms import ProductForm

from flask import Blueprint

products = Blueprint('products', __name__)


@products.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
	form = ProductForm()
	if form.validate_on_submit():
		# TODO: Scrape Amazon for other info
		product = Product(name="Dummy name", seller="Amazon Mexico", currency_code="MXN", current_price=385, optimal_price=form.optimal_price.data, available=True, link=form.link.data, author=current_user)
		db.session.add(product)
		db.session.commit()
		flash("Product added successfully.", 'success');
		return redirect(url_for('main.home'))
	return render_template('add_product.html', title="Add Product", form=form)


@products.route('/product/<int:product_id>')
def product(product_id):
	product = Product.query.get_or_404(product_id)
	return render_template('product.html', title=product.name, product=product)


@products.route('/product/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
	product = Product.query.get_or_404(product_id)
	if product.author != current_user:
		abort(403)
	form = ProductForm()
	if form.validate_on_submit():
		product.link = form.link.data
		product.optimal_price = form.optimal_price.data
		db.session.commit()
		flash("Update successful.", 'success')
		return redirect(url_for('products.product', product_id=product.id))
	if request.method == 'GET':
		form.link.data = product.link
		form.optimal_price.data = product.optimal_price
	return render_template('add_product.html', title="Update Product", form=form)


@products.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
	product = Product.query.get_or_404(product_id)
	if product.author != current_user:
		abort(403)
	db.session.delete(product)
	db.session.commit()
	flash("Deletion successful", 'success')
	return redirect(url_for('main.home'))
