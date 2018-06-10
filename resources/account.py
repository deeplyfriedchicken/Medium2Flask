import sqlite3
from flask_restful import Resource

from models.account import AccountModel


class Account(Resource):
    def get(self, name):
        account = AccountModel.find_by_name(name)
        if account:
            return account.json()
        else:
            return {'message': 'Account not found'}, 404


class AccountList(Resource):
    """Lists the items"""
    def get(self):
        accounts = [account.json() for account in AccountModel.find_all()]
        return {
          'accounts': accounts
        }
