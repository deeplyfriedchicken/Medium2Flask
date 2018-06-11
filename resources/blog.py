import sqlite3
from flask_restful import Resource

from models.blog import PostModel, CategoryModel


class Post(Resource):
    def get(self, name):
        post = PostModel.find_by_name(name)
        if post:
            return post.json()
        else:
            return {'message': 'Post not found'}, 404

    # delete + JWT

class PostList(Resource):
    """Lists the items"""
    def get(self):
        posts = [post.json() for post in PostModel.find_all_active()]
        return {
            'posts': posts
        }

class PostCategoryList(Resource):
    """Lists the items by a specified category"""
    def get(self, category):
        posts = [post.json() for post in PostModel.find_by_category(category)]
        return {
            'posts': posts
        }

class PostAccountList(Resource):
    """Lists the items"""
    def get(self, name):
        posts = [post.json() for post in PostModel.find_by_account(name)]
        return {
            'posts': posts
        }


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
        categories = [category.name for category in CategoryModel.find_all()]
        return {
          'categories': categories
        }