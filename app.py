from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@db:5432/parkingdb'
db = SQLAlchemy()
db.init_app(app)


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


with app.app_context():
    db.create_all()


class Users(Resource):
    def get(self):
        users = UserModel.query.all()
        return users


api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
