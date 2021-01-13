from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from flask_login import current_user, login_required
from app import db, q
from app.models import User, Product
from app.products.forms import ProductForm
from app.products.utils import get_product_data
# import redis
# from rq import Queue
from rq.job import Job
# from worker import conn

products = Blueprint('products', __name__)


@products.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
	form = ProductForm()
	return render_template('add_product.html', title="Add Product", form=form, active=2)


@products.route('/product/add', methods=['POST'])
@login_required
def add_product():
	form = ProductForm()
	print("FORM CREATED")
	if form.validate_on_submit():
		print("FORM VALIDATED")
		if Product.query.count() < 20: # max total products
			print("DATABASE FREE")
			if Product.query.filter_by(author=current_user).count() < 10: # max concurrent products
				print("LIMIT NOT REACHED")
				form_data = {'link': form.link.data, 'optimal_price': form.optimal_price.data, 'user_id': current_user.id}
				print("FORM DATA RETRIEVED:")
				print(form_data['link'], form_data['optimal_price'], form_data['user_id'])
				job = q.enqueue(get_product_data, form_data)
				print("JOB ENQUEUED")
				return jsonify(location=url_for('products.job_status', job_id=job.get_id()))
			else:
				print("LIMIT REACHED")
				flash("Sorry. You've reached your product limit.", 'warning')
				print("FLASHED 1")
		else:
			print("DATABASE FULL")
			flash("Sorry. Our database is full at the moment.", 'info')
			print("FLASHED 2")
	print("ERRORS DETECTED")
	return jsonify(error=form.errors) # could return nothing in some cases.


@products.route("/status/<job_id>", methods=['GET'])
@login_required
def job_status(job_id):
	job = q.fetch_job(job_id)
	if not job:
		response = {'status': 'unknown'}
	elif job.result is False:
		response = {'status': 'invalid'}
	else:
		response = {
			'status': job.get_status(),
			'image': job.result
		}
        # if job.is_failed:
            # response['message'] = job.exc_info.strip().split('\n')[-1]
	return jsonify(response)


# @products.route('/product/<int:product_id>')
# def product(product_id):
# 	product = Product.query.get_or_404(product_id)
# 	return render_template('product.html', title=product.name, product=product)


# TODO: Rewrite this whole thing
@products.route('/product/<int:product_id>/update', methods=['POST'])
@login_required
def update_product(product_id):
	product = Product.query.get_or_404(product_id)
	if product.author != current_user:
		abort(403)
	form = ProductForm()
	form.link.data = product.link
	if form.validate_on_submit():
		product.optimal_price = form.optimal_price.data
		db.session.commit()
		flash("Update successful.", 'success')
		return jsonify(status="successful")
	return jsonify(error=form.errors) # could return nothing in some cases.


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
