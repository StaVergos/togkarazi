from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from marshmallow import ValidationError
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from ma import ma
from db import db
from blocklist import BLOCKLIST

from resources.user import UserLogin, UserLogout, TokenRefresh, UserRegister

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


# Callback function to check if a JWT exists in the blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(decrypted_token):
    return decrypted_token['jti'] in BLOCKLIST


api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refreshlogin')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister, '/register')


db.init_app(app)

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
