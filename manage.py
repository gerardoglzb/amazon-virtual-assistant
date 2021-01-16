import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.config import Config

app = create_app()
with app.app_context():
	from app import models
	db.create_all()

	app.config.from_object(Config)

	migrate = Migrate(app, db)
	manager = Manager(app)

	manager.add_command('db', MigrateCommand)


	if __name__ == '__main__':
		manager.run()