from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.post import Post, PostList
from resources.category import Category, CategoryList
from resources.account import Account, AccountList

from secrets import DB_PATH, SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = SECRET_KEY
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)  # not creating /auth

api.add_resource(PostList, '/api/posts')
api.add_resource(Category, '/api/category')
api.add_resource(Account, '/api/account/<string:name>')
api.add_resource(AccountList, '/api/accounts')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

