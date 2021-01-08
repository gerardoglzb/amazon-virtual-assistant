from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(30), nullable=False)
	products = db.relationship('Product', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
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

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"


class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(500), nullable=False)
	seller = db.Column(db.String(100), nullable=False)
	currency_code = db.Column(db.String(3), nullable=False)
	current_price = db.Column(db.String(15), nullable=False)
	optimal_price = db.Column(db.Float, nullable=False)
	available = db.Column(db.String(100), nullable=False, default=True)
	link = db.Column(db.String(1000), nullable=False)
	img = db.Column(db.String(1000), default="https://static.im-a-puzzle.com/gallery/Animals/Dogs/Puppy-dog-cream.jpg")
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Product('{self.name}', '{self.seller}')"