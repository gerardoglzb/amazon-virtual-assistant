from flask import flash, url_for, jsonify
from flask_login import current_user
from app import db, create_app
from app.models import User, Product
import requests
from bs4 import BeautifulSoup
import json
import random
import re
import time
from datetime import datetime


def send_product_notification():
	print("sending product notification...")


def update_products():
	app = create_app()
	now = datetime.utcnow()
	with app.app_context():
		for product in Product.query.all():
			data = update_product_data(product.link, product.optimal_price)
			product.price = data['price']
			product.available = data.get('availability', "")
			if not product.last_notification or (now - product.last_notification).days >= 3:
				if product.price <= product.optimal_price:
					product.last_notification = now
					send_product_notification()
			if (now - product.date_added).days >= 30:
				db.session.delete(product)
			time.sleep(10)
		db.session.commit()


def update_product_data(url, optimal_price):
	user_agents = [
		# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
	]

	user_agent = random.choice(user_agents)
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "es-ES,es;q=0.9,en;q=0.8", "Referer": "http://www.google.com/", "User-Agent": user_agent}
	source = requests.get(url, headers=headers, timeout=10)

	# TODO: Handle this
	if source.status_code != 200:
		return False

	soup = BeautifulSoup(source.text, "lxml")
	data = {}

	price_el = soup.find(id="price_inside_buybox")
	price_temp = price_el.get_text(strip=True) if price_el else None
	price_string = price_temp.replace(u'\xa0', u' ') if price_temp else None
	price_matches = re.findall(r"[-+]?\d*\.\d+|\d+", price_string) if price_string else None # Accepts negative numbers, just in case.
	price = float(price_matches[0]) if len(price_matches) == 1 else None
	if price:
		data['price'] = price
	else:
		data['price'] = -1

	availability_el_el = soup.find(id="availability")
	availability_el = availability_el_el.find("span") if availability_el_el else None
	availability = availability_el.get_text(strip=True) if availability_el else ""
	if availability:
		data['availability'] = availability

	return data


def get_product_data(form_data):
	# TODO: Make sure form_data has link and optimal_price.
	user_agents = [
		# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
	]

	user_agent = random.choice(user_agents)
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "es-ES,es;q=0.9,en;q=0.8", "Referer": "http://www.google.com/", "User-Agent": user_agent}
	source = requests.get(form_data['link'], headers=headers, timeout=10)

	# TODO: Handle this
	if source.status_code != 200:
		return False

	soup = BeautifulSoup(source.text, "lxml")
	data = {}

	name_el = soup.find(id="productTitle")
	name = name_el.get_text(strip=True) if name_el else None
	if name:
		data['name'] = name
	else:
		# Couldn't find name
		return

	seller_el = soup.find(id="sellerProfileTriggerId")
	seller = seller_el.get_text(strip=True) if seller_el else None
	if seller:
		data['seller'] = seller

	price_el = soup.find(id="price_inside_buybox")
	price_temp = price_el.get_text(strip=True) if price_el else None
	price_string = price_temp.replace(u'\xa0', u' ') if price_temp else None
	price_matches = re.findall(r"[-+]?\d*\.\d+|\d+", price_string) if price_string else None
	price = float(price_matches[0]) if len(price_matches) == 1 else None
	if price:
		data['price'] = price
	else:
		# Couldn't find prize
		return

	# shipping_el_el = soup.find(id="ourprice_shippingmessage")
	# shipping_el = shipping_el_el.find("span") if shipping_el_el else None
	# shipping = shipping_el.get_text(strip=True) if shipping_el else ""

	image_el = soup.find(id="landingImage")
	image_json = image_el['data-a-dynamic-image'] if image_el else None
	image_dict = json.loads(image_json) if image_json else None
	image_list = list(image_dict.keys()) if image_dict else None
	image = image_list[-1] if image_list else ""
	if image:
		data['image'] = image

	availability_el_el = soup.find(id="availability")
	availability_el = availability_el_el.find("span") if availability_el_el else None
	availability = availability_el.get_text(strip=True) if availability_el else ""
	if availability:
		data['availability'] = availability

	currency_el_el = soup.find(id="icp-touch-link-cop")
	currency_el = currency_el_el.find("span", class_="icp-color-base") if currency_el_el else None
	currency = currency_el.get_text(strip=True) if currency_el else None
	currency_code = currency.split(' ', 1)[0] if currency else ""
	if currency_code:
		data['currency_code'] = currency_code

	data['link'] = form_data['link']
	data['optimal_price'] = float(form_data['optimal_price'])

	app = create_app()
	with app.app_context():
		author = User.query.get(form_data['user_id'])
		product = Product(name=data.get('name', "Unknown product"), seller=data.get('seller', "Unknown seller"), currency_code=data.get('currency_code', ""), current_price=data.get('price', "-1"), optimal_price=data.get('optimal_price', -1.0), available=data.get('availability', ""), link=data.get('link', "amazon.com"), author=author)
		product.img = data.get('image', product.img)
		db.session.add(product)
		db.session.commit()
