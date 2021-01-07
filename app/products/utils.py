import requests
from bs4 import BeautifulSoup
import json
import random

user_agents = [
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
	"Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
	"Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
	"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
	"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
	"Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
	"Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36",
	"Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36",
	"Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7",
	"Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"
]


def get_product_data(url, user_agents):
	user_agent = random.choice(user_agents)
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "es-ES,es;q=0.9,en;q=0.8", "Referer": "http://www.google.com/", "User-Agent": user_agent}
	source = requests.get(url, headers=headers, timeout=10)

	if source.status_code != 200:
		return False

	soup = BeautifulSoup(source.text, "lxml")
	data = {}

	name_el = soup.find(id="productTitle")
	name = name_el.get_text(strip=True) if name_el else None
	if name:
		data['name'] = name

	seller_el = soup.find(id="sellerProfileTriggerId")
	seller = seller_el.get_text(strip=True) if seller_el else None
	if seller:
		data['seller'] = seller

	price_el = soup.find(id="price_inside_buybox")
	price_temp = price_el.get_text(strip=True) if price_el else None
	price = price_temp.replace(u'\xa0', u' ') if price_temp else None
	if price:
		data['price'] = price

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

	return data


def update_product_data(url, user_agents):
	user_agent = random.choice(user_agents)
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "es-ES,es;q=0.9,en;q=0.8", "Referer": "http://www.google.com/", "User-Agent": user_agent}
	source = requests.get(url, headers=headers, timeout=10)

	if source.status_code != 200:
		return False

	soup = BeautifulSoup(source.text, "lxml")
	data = {}

	price_el = soup.find(id="price_inside_buybox")
	price_temp = price_el.get_text(strip=True) if price_el else None
	price = price_temp.replace(u'\xa0', u' ') if price_temp else None
	if price:
		data['price'] = price

	availability_el_el = soup.find(id="availability")
	availability_el = availability_el_el.find("span") if availability_el_el else None
	availability = availability_el.get_text(strip=True) if availability_el else ""
	if availability:
		data['availability'] = availability

	return data
