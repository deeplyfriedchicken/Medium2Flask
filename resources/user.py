"""This module creates the user class for authentication"""
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_refresh_token_required,
                                jwt_required,
                                get_jwt_identity,
                                get_raw_jwt)

from models.user import UserModel

from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="Username is required")
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="Password is required")


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_username_or_id('id', user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_username_or_id('id', user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


class UserRegister(Resource):
    """Class to handle user registers via API"""
    def post(self):
        """Creates a new user on signup"""
        data = _user_parser.parse_args()

        if (UserModel.find_by_username_or_id('username',
                                             data['username']) is not None):
            message = "This username already exists"
            return {"message": message}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    @classmethod
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username_or_id('username', data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        """Blacklist their current access token so they have to get a new one"""
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identitfier for JWT
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200