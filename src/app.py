from flask import jsonify
from flask_restful import Resource, reqparse
import uuid

from .models import ParkingModel

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
        return jsonify(response)
