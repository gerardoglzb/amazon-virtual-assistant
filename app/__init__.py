from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
import redis
from rq import Queue
from rq.job import Job
from worker import conn
from apscheduler.schedulers.background import BackgroundScheduler


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
q = Queue(connection=conn, default_timeout=1800)


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	print("here we gooooooo")
	print(app.config['SQLALCHEMY_DATABASE_URI'])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	from app import models

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from app.users.routes import users
	from app.products.routes import products
	from app.main.routes import main
	from app.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(products)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	from app.products.utils import update_products

	# TODO: Uncomment this for production mode.
	# scheduler = BackgroundScheduler()
	# scheduler.add_job(update_products, trigger='interval', hours=6, id='update_products_id', replace_existing=True)
	# scheduler.start()

	return app
