import os
# import secrets
from flask import url_for
from flask_mail import Message
from app import mail

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender=os.environ.get('EMAIL_USER'), recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link: 
{url_for('reset_token', token=token, _external=True)}

If you did not request this change, ignore this email.
	'''
	mail.send(msg)
