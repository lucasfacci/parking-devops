from flask import Flask
from flask_restful import Api

from .app import HealthCheck, Parking, Parkings
from .db import init_db


def create_app(config):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config)
    init_db(app)

    api.add_resource(HealthCheck, "/health")
    api.add_resource(Parkings, "/parkings")
    api.add_resource(Parking, "/parking", "/parking/<string:uuid>")

    return app
