import sqlite3
from flask_restful import Resource

from models.post import PostModel


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
        posts = [post.json() for post in PostModel.find_all()]
        return {
            'posts': posts
        }
