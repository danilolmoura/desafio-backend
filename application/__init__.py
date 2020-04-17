import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp

from config import config_by_name

db = SQLAlchemy()

from application import db

from application.models import User

def create_app(config_name):
    from flask_potion import Api

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    app.logger.info('Connecting database')
    db.init_app(app)

    app.logger.info('Setting authenticator')
    def authenticate(email, password):
        import pdb
        pdb.set_trace()
        user = User.query.filter_by(
            email=email
        ).first()

        if user and safe_str_cmp(
                user.password.encode('utf-8'),
                password.encode('utf-8')):
            return user

    def identity(payload):
        user_id = payload['identity']
        return User.query.get(user_id)

    jwt = JWT(app, authenticate, identity)

    app.logger.info('creating Flask-Potion Apis')
    from application import apis
    api = Api(app, prefix='/api/v1', title='Backend API')
    apis.create_api(api)

    app.logger.info('Finished initialization')

    return app