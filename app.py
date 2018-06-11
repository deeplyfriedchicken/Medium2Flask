from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources.blog import Post, PostList, PostAccountList, PostCategoryList, CategoryList
from resources.account import Account, AccountList
from resources.user import UserLogin, UserLogout

from actions.register_user import registerUser

from blacklist import BLACKLIST

from secrets import DB_PATH, SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = SECRET_KEY
api = Api(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.before_first_request
def create_tables():
    db.create_all()
    registerUser()

jwt = JWTManager(app)  # not creating /auth


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Determines if blacklisted and redirects to revoked token loader if so"""
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed. Invalid token detected.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh. Please login again.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    """When a user logouts, it revokes the token"""
    return jsonify({
        'description': 'The token is not fresh. Please login again.',
        'error': 'token_revoked'
    })


api.add_resource(PostList, '/api/posts')
api.add_resource(PostCategoryList, '/api/posts/category/<string:category>')
api.add_resource(PostAccountList, '/api/posts/account/<string:name>')
api.add_resource(CategoryList, '/api/categories')
api.add_resource(Account, '/api/account/<string:name>')
api.add_resource(AccountList, '/api/accounts')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

