import os

from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
#from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from db import db

# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemsList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config['JWT_AUTH_URL_RULE'] = '/login'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'cris'
api = Api(app)

# jwt = JWT(app, authenticate, identity) # Create a /auth endpoint by itself.
jwt = JWTManager(app)

# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#     return jsonify({
#                         'access_token': access_token.decode('utf-8'),
#                         'user_id': identity.id
#                    })

# @jwt.jwt_error_handler
# def customized_error_handler(error):
#     return jsonify({
#                        'message': error.description,
#                        'code': error.status_code
#                    }), error.status_code    

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)