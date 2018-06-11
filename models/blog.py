import sqlite3
from db import db
from sqlalchemy import and_, desc

from flask_restful import url_for

from models.account import AccountModel

association_table = db.Table('posts_categories', db.Model.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    account = db.relationship('AccountModel')
    title = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime)
    link = db.Column(db.String(300))
    author = db.Column(db.String(80))
    thumbnail = db.Column(db.String(300))
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    categories = db.relationship('CategoryModel', secondary=association_table)
    

    def __init__(self, account_id, title, pub_date, link, author, thumbnail, description, content, categories = []):
        self.account_id = account_id
        self.title = title
        self.pub_date = pub_date
        self.link = link
        self.author = author
        self.thumbnail = thumbnail
        self.description = description
        self.content = content
        self.categories = categories

    def json(self):
        categories = [category.name for category in self.categories]
        return {
            'id': self.id,
            'account': self.account.name,
            'title': self.title,
            'pub_date': self.pub_date.__str__(),
            'link': self.link,
            'author': self.author,
            'thumbnail': self.thumbnail,
            'description': self.description,
            'categories': categories
        }

    @classmethod
    def paginate(cls, page):
        paginate = cls.find_all_active().paginate(page, 5, False)
        next_url = url_for('api.post_list', page=paginate.next_num) if paginate.has_next else None
        prev_url = url_for('api.post_list', page=paginate.prev_num) if paginate.has_prev else None
        return {
            'posts': paginate.items,
            'next': next_url,
            'prev': prev_url
        }

    @classmethod
    def paginate_by_account(cls, name, page):
        paginate = cls.find_by_account(name).paginate(page, 5, False)
        next_url = url_for('api.post_account_list', page=paginate.next_num, name=name) if paginate.has_next else None
        prev_url = url_for('api.post_account_list', page=paginate.prev_num, name=name) if paginate.has_prev else None
        return {
            'posts': paginate.items,
            'next': next_url,
            'prev': prev_url
        }

    @classmethod
    def paginate_by_category(cls, category, page):
        paginate = cls.find_by_category(category).paginate(page, 5, False)
        next_url = url_for('api.post_category_list', page=paginate.next_num, category=category) if paginate.has_next else None
        prev_url = url_for('api.post_category_list', page=paginate.prev_num, category=category) if paginate.has_prev else None
        return {
            'posts': paginate.items,
            'next': next_url,
            'prev': prev_url
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_active(cls):
        return cls.query.filter(cls.account.has(is_active=True)).order_by(desc(cls.pub_date))

    @classmethod
    def find_by_account(cls, account_name):
        return cls.query.filter(cls.account.has(name=account_name)).order_by(desc(cls.pub_date))

    @classmethod
    def find_by_category(cls, category_name):
        return cls.query.filter(and_(cls.account.has(is_active=True), cls.categories.any(CategoryModel.name.contains(category_name)))).order_by(desc(cls.pub_date))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_or_create(cls, name):
        category = cls.query.filter_by(name=name).first()
        if category is None:
            category = CategoryModel(name)
        return category

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
