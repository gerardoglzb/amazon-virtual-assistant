import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY', '12345')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres@localhost/amazonva_dev')
	# SQLALCHEMY_DATABASE_URI = 'postgresql://post'
	print(os.environ.get('DATABASE_URL'))
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')