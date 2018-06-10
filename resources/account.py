import sqlite3
from flask_restful import Resource, reqparse, inputs

from models.account import AccountModel


class Account(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('is_active',
                        type=inputs.boolean,
                        required=True,
                        help="This account needs an is_active boolean.")


    def get(self, name):
        account = AccountModel.find_by_name(name)
        if account:
            return account.json()
        else:
            return {'message': 'Account not found'}, 404
    
    def post(self, name):
        if AccountModel.find_by_name(name):
            return {
              "message": "An item with name '{}' already exists."
              .format(name)}, 400

        data = Account.parser.parse_args()

        account = AccountModel(name, **data)

        try:
            account.save_to_db()
        except:
            return {"message": "An error occurred adding the account."}, 500

        return account.json(), 201

    def delete(self, name):
        account = AccountModel.find_by_name(name)
        if account:
            account.delete_from_db()

        return {'message': "Account deleted"}


class AccountList(Resource):
    """Lists the items"""
    def get(self):
        accounts = [account.json() for account in AccountModel.find_all()]
        return {
          'accounts': accounts
        }
