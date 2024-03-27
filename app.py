from datetime import datetime
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'parkingdb',
    'host': 'mongodb',
    'port': 27017,
    'username': 'root',
    'password': 'root'
}

api = Api(app)
db = MongoEngine(app)


class ParkingModel(db.Document):
    id = db.UUIDField(required=True, unique=True)
    plate = db.StringField(required=True)
    brand = db.StringField(required=True)
    model = db.StringField(required=True)
    color = db.StringField(required=True)
    entry = db.DateTimeField(required=True, default=datetime.now)
    exit = db.DateTimeField()
    status = db.StringField(required=True)
    total_amount = db.DecimalField(precision=2)


class Parkings(Resource):
    def get(self):
        return {"message": "parkings"}


class Parking(Resource):
    def get(self, id):
        return {'message', 'parking'}


api.add_resource(Parkings, '/parkings')
api.add_resource(Parking, '/parking', '/parking/<string:id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
