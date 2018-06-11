import sqlite3
from db import db
from sqlalchemy import and_

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
    categories = db.relationship('CategoryModel', secondary=association_table)
    

    def __init__(self, account_id, title, pub_date, link, author, thumbnail, description, categories = []):
        self.account_id = account_id
        self.title = title
        self.pub_date = pub_date
        self.link = link
        self.author = author
        self.thumbnail = thumbnail
        self.description = description
        self.categories = categories

    def json(self):
        categories = [category.name for category in self.categories]
        return {
            'id': self.id,
            'account_id': self.account_id,
            'title': self.title,
            'publication_date': self.pub_date.__str__(),
            'link': self.link,
            'author': self.author,
            'thumbnail': self.thumbnail,
            'description': self.description,
            'categories': categories
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_active(cls):
        return cls.query.filter(cls.account.has(is_active=True))

    @classmethod
    def find_by_account(cls, account_name):
        account = AccountModel.find_by_name_and_active(account_name)
        if account is None:
            return []
        return cls.query.filter_by(account_id=account.id)

    @classmethod
    def find_by_category(cls, category_name):
        category = CategoryModel.find_by_name(category_name)
        if category is None:
            return []
        return cls.query.filter(and_(cls.account.has(is_active=True), cls.categories.any(id=category.id)))

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
