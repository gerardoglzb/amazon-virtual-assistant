from apscheduler.schedulers.blocking import BlockingScheduler
from app import create_app

app = create_app()
with app.app_context():
	from app.products.utils import update_products

	scheduler = BlockingScheduler()

	@sched.scheduled_job('cron', day_of_week='mon-sun', hour='0,6,12,18', id='update_products_id', replace_existing=True)
	def update_products_job():
		update_products()

	scheduler.start()
