import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config_by_name

db = SQLAlchemy()

from application import db

def create_app(config_name):
	from flask_potion import Api

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(config_by_name[config_name])

	app.logger.info('Connecting database')
	db.init_app(app)

	app.logger.info('Defining default URL')
	@app.route('/')
	def index():
		return "Welcome to Backend API!"

	app.logger.info('Finished initialization')

	return app