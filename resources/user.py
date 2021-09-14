from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

import traceback

from blocklist import BLOCKLIST
from models import user

from schemas.user import UserSchema
from models.user import UserModel
from libs.strings import gettext


user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)
        try:
            user.save_to_db()
            return {"message": gettext("user_registered")}, 201
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {"message": gettext("user_error_creating")}, 500


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            user_json = request.get_json()
            user_data = user_schema.load(user_json, partial=("email",))
        except ValidationError as err:
            return err.messages, 400

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user_data.password, user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return (
                {"access_token": access_token, "refresh_token": refresh_token},
                200,
            )

        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        BLOCKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
