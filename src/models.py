from datetime import datetime

from .db import db


class HealthCheckModel(db.Document):
    status = db.StringField(required=True)


class ParkingModel(db.Document):
    uuid = db.UUIDField(binary=False, required=True)
    plate = db.StringField(required=True)
    brand = db.StringField(required=True)
    model = db.StringField(required=True)
    color = db.StringField(required=True)
    entry = db.DateTimeField(default=datetime.now)
    exit = db.DateTimeField()
    status = db.StringField(required=True)
    total_amount = db.DecimalField(precision=2)
