import sqlite3
from flask_restful import Resource
from flask import request

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
    """Paginates the posts"""
    def get(self):
        page = request.args.get('page', 1, type=int)
        paginate = PostModel.paginate(page)
        posts = [post.json() for post in paginate['posts']]
        return {
            'next': paginate['next'],
            'prev': paginate['prev'],
            'posts': posts
        }

class PostCategoryList(Resource):
    """Paginates the posts by a specified category"""
    def get(self, category):
        page = request.args.get('page', 1, type=int)
        paginate = PostModel.paginate_by_category(category, page)
        posts = [post.json() for post in paginate['posts']]
        return {
            'next': paginate['next'],
            'prev': paginate['prev'],
            'posts': posts
        }

class PostAccountList(Resource):
    """Paginates the posts by a specified account"""
    def get(self, name):
        page = request.args.get('page', 1, type=int)
        paginate = PostModel.paginate_account(name, page)
        posts = [post.json() for post in paginate['posts']]
        return {
            'next': paginate['next'],
            'prev': paginate['prev'],
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