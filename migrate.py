from flask import Flask

from configuration import Configuration

from models import database

from flask_migrate import Migrate

application = Flask(__name__)
application.config.from_object(Configuration)

database.init_app(application)

migrate = Migrate(application, database)
