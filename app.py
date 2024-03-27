from datetime import datetime
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api, reqparse
import uuid

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

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('plate',
                          type=str,
                          required=True,
                          help='This field cannot be blank.')
_user_parser.add_argument('brand',
                          type=str,
                          required=True,
                          help='This field cannot be blank.')
_user_parser.add_argument('model',
                          type=str,
                          required=True,
                          help='This field cannot be blank.')
_user_parser.add_argument('color',
                          type=str,
                          required=True,
                          help='This field cannot be blank.')
_user_parser.add_argument('exit',
                          type=str,
                          required=False,
                          help='This field cannot be blank.')
_user_parser.add_argument('status',
                          type=str,
                          required=True,
                          help='This field cannot be blank.')
_user_parser.add_argument('total_amount',
                          type=str,
                          required=False,
                          help='This field cannot be blank.')


class ParkingModel(db.Document):
    uuid = db.UUIDField(binary=False, required=True)
    plate = db.StringField(required=True)
    brand = db.StringField(required=True)
    model = db.StringField(required=True)
    color = db.StringField(required=True)
    entry = db.DateTimeField(default=datetime.now)
    exit = db.DateTimeField()
    status = db.StringField(required=True)
    total_amount = db.DecimalField(default=5.00, precision=2)


class Parkings(Resource):
    def get(self):
        return jsonify(ParkingModel.objects())


class Parking(Resource):
    def generate_uuid(self, data):
        uuid_dict = {'uuid': uuid.uuid4()} | data
        return uuid_dict

    def get(self, uuid):
        response = ParkingModel.objects(uuid=uuid)

        if response:
            return jsonify(response)

        return {'message': 'Parking not found.'}

    def post(self):
        data = _user_parser.parse_args()
        data = self.generate_uuid(data)
        response = ParkingModel(**data).save()
        return jsonify({
            'uuid': response.uuid,
            'plate': response.plate,
            'brand': response.brand,
            'model': response.model,
            'color': response.color,
            'entry': response.entry.isoformat(),
            'exit': response.exit.isoformat() if response.exit else None,
            'status': response.status,
            'total_amount': response.total_amount
        })


api.add_resource(Parkings, '/parkings')
api.add_resource(Parking, '/parking', '/parking/<string:uuid>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
