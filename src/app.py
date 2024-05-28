from datetime import datetime
from flask import jsonify, make_response
from flask_restful import Resource, reqparse
import uuid

from .models import HealthCheckModel, ParkingModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "plate", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "brand", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "model", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "color", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "entry",
    type=(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")),
    required=False,
    help=("'This field must be of type datetime " "(e.g. %Y-%m-%dT%H:%M:%S).'"),
)
_user_parser.add_argument(
    "exit",
    type=(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")),
    required=False,
    help=("'This field must be of type datetime " "(e.g. %Y-%m-%dT%H:%M:%S).'"),
)
_user_parser.add_argument(
    "status", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "total_amount", type=int, required=False, help="This field must be of type int."
)


class HealthCheck(Resource):
    def get(self):
        response = HealthCheckModel.objects(status="healthcheck")
        if not response:
            HealthCheckModel(status="healthcheck").save()
        return "Healthy", 200


class Parkings(Resource):
    def get(self):
        return jsonify(ParkingModel.objects())


class Parking(Resource):
    def generate_uuid(self, data):
        uuid_dict = {"uuid": uuid.uuid4()} | data
        return uuid_dict

    def calculate_total_amount(self, entry, exit):
        time_difference = exit - entry
        # Convert into hours
        total_hours = time_difference.total_seconds() / 3600

        # If less than 20 minutes
        if total_hours < (20 / 60):
            return 0

        # Calculate the fraction of an hour
        whole_hours = int(total_hours)
        fraction_hour = total_hours - whole_hours

        # Calculate the amount to pay based in the hours
        total_amount = 24.00
        for i in range(whole_hours - 2):
            total_amount += 4.00

        # Sums in the amount to pay if there's a fraction of an hour
        if whole_hours >= 2 and fraction_hour > 0:
            total_amount += 4.00

        return total_amount

    def post_and_put_validations(self, data):
        if data["status"] != "parked" and data["status"] != "left":
            return {
                "error": True,
                "output": {
                    "message": (
                        "The 'status' field can only accept "
                        "'parked' or 'left' values."
                    )
                },
            }

        if data.get("entry") is not None and data.get("exit") is not None:
            if data["exit"] < data["entry"]:
                return {
                    "error": True,
                    "output": {
                        "message": (
                            "The 'exit' datetime field cannot be from "
                            "before than the 'entry' datetime field."
                        )
                    },
                }

        if data["status"] == "parked" and data.get("exit") is not None:
            return {
                "error": True,
                "output": {
                    "message": (
                        "The 'exit' field cannot be assigned if "
                        "the 'status' field is 'parked'."
                    )
                },
            }

        return {"error": False}

    def calculate_fields(self, parking, data):
        if (
            data["status"] == "left"
            and data.get("exit") is None
            and data.get("total_amount") is None
        ):

            if parking.exit is None:
                parking.exit = datetime.now()
            if parking.total_amount is None:
                parking.total_amount = self.calculate_total_amount(
                    parking.entry, parking.exit
                )

        if data.get("exit") is not None and data.get("total_amount") is None:
            if parking.total_amount is None:
                parking.total_amount = self.calculate_total_amount(
                    parking.entry, parking.exit
                )

    def get(self, uuid):
        try:
            parking = ParkingModel.objects.get(uuid=uuid)
        except ParkingModel.DoesNotExist:
            return {"message": "Parking not found."}, 404

        return jsonify(parking)

    def post(self):
        data = _user_parser.parse_args()
        data = self.generate_uuid(data)

        # Validation
        validation_output = self.post_and_put_validations(data)
        if validation_output["error"] is True:
            return validation_output["output"], 400

        parking = ParkingModel(**data)

        # Calculated fields
        self.calculate_fields(parking, data)

        parking.save()
        return make_response(jsonify(parking), 201)

    def put(self, uuid):
        data = _user_parser.parse_args()
        try:
            parking = ParkingModel.objects.get(uuid=uuid)
        except ParkingModel.DoesNotExist:
            return {"message": "Parking not found."}, 404

        # Required fields
        parking.plate = data["plate"]
        parking.brand = data["brand"]
        parking.model = data["model"]
        parking.color = data["color"]
        parking.status = data["status"]

        # Validation
        validation_output = self.post_and_put_validations(data)
        if validation_output["error"] is True:
            return validation_output["output"], 400

        # Calculated fields
        self.calculate_fields(parking, data)

        # Optional fields
        if data.get("entry") is not None:
            parking.entry = data["entry"]
        if data.get("exit") is not None:
            parking.exit = data["exit"]
        if data.get("total_amount") is not None:
            parking.total_amount = data["total_amount"]

        parking.save()
        return make_response(jsonify(parking), 201)

    def delete(self, uuid):
        try:
            ParkingModel.objects.get(uuid=uuid).delete()
        except ParkingModel.DoesNotExist:
            return {"message": "Parking not found."}, 404

        return "", 204
