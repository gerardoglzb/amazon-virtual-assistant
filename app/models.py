from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	__tablename__ = 'app_user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(300), nullable=False)
	products = db.relationship('Product', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"


class Product(db.Model):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(500), nullable=False)
	seller = db.Column(db.String(100), nullable=False)
	currency_code = db.Column(db.String(3), nullable=False)
	current_price = db.Column(db.Float, nullable=False)
	optimal_price = db.Column(db.Float, nullable=False)
	available = db.Column(db.String(100), nullable=False, default=True)
	link = db.Column(db.String(1000), nullable=False)
	img = db.Column(db.String(1000), default="https://static.im-a-puzzle.com/gallery/Animals/Dogs/Puppy-dog-cream.jpg")
	date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	last_notification = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)

	def __init__(self, name, seller, currency_code, current_price, optimal_price, available, link, author):
		self.name = name
		self.seller = seller
		self.currency_code = currency_code
		self.current_price = current_price
		self.optimal_price = optimal_price
		self.available = available
		self.link = link
		self.author = author

	def __repr__(self):
		return f"Product('{self.name}', '{self.seller}')"