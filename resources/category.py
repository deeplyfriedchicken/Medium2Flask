import sqlite3
from flask_restful import Resource

from models.category import CategoryModel


class Category(Resource):
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        else:
            return {'message': 'Category not found'}, 404


class CategoryList(Resource):
    """Lists the items"""
    def get(self):
        categories = [category.json() for category in CategoryModel.find_all()]
        return {
          'categories': categories
        }
