import sqlite3
from db import db


class AccountModel(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    is_active = db.Column(db.Boolean)

    posts = db.relationship('PostModel', lazy='dynamic')

    def __init__(self, name, is_active = True):
        self.name = name
        self.is_active = is_active

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_all_active(cls):
        return cls.query.fitler_by(is_active=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()