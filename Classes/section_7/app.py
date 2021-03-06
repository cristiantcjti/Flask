import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError
from dotenv import load_dotenv


from db import db
from ma import ma
from resources.user import UserRegister, UserLogin, User


app = Flask(__name__)
load_dotenv(".env")
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://cris:postgres@localhost:5432/flask_db' # os.environ.get(
#    "DATABASE_URI", "sqlite:///data.db"
#)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "jose"
db.init_app(app) #
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    ma.init_app(app)
    #db.init_app(app) #
    app.run(port=5000, debug=True)
