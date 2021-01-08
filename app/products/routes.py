from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from flask_login import current_user, login_required
from app import db, q
from app.models import Product
from app.products.forms import ProductForm
from app.products.utils import get_product_data
# import redis
# from rq import Queue
from rq.job import Job
# from worker import conn

products = Blueprint('products', __name__)


@products.route('/product/new', methods=['GET'])
@login_required
def new_product():
	form = ProductForm()
	return render_template('add_product.html', title="Add Product", form=form)


@products.route('/product/add', methods=['POST'])
@login_required
def add_product():
	form = ProductForm()
	if form.validate_on_submit():
		job = q.enqueue(get_product_data, form.link.data)
		# data = get_product_data(form.link.data)
		# product = Product(name=data.get('name', "Unknown product"), seller=data.get('seller', "Unknown seller"), currency_code=data.get('currency_code', ""), current_price=data.get('price', -1), optimal_price=form.optimal_price.data, available=data.get('availability', ""), link=form.link.data, author=current_user)
		# product.img = data.get('image', product.img)
		# db.session.add(product)
		# db.session.commit()
		# flash("Product added successfully.", 'success');
		# return redirect(url_for('main.home'))
		return jsonify(location=url_for('products.job_status', job_id=job.get_id()))
	return jsonify(data=form.errors)


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
