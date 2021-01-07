from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Product
from app.users.forms import RegistrationForm, LoginForm, UpdateForm, RequestResetForm, ResetForm
from app.users.utils import send_reset_email

from flask import Blueprint

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f"Registration successful.", 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title="Register", form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			flash("Login successful.", 'success')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		flash("Login unsuccessful. Check email and password.", 'danger')
	return render_template('login.html', title="Login", form=form)


@users.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	form = UpdateForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Update successful.", 'success')
		return redirect(url_for('users.account'))
	if request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('profile.html', title="Profile", form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("Reset email sent.", 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title="Reset Password", form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if not user:
		flash("Invalid or expired token", 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f"Password reset successful.", 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title="Reset Password", form=form)