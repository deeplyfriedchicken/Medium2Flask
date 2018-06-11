import sqlite3
from db import db

from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, email, password):
        self.email = email
        self.password = self.set_password(password)

    def json(self):
        return {
            'id': self.id,
            'email': self.email
        }

    def set_password(self, password):
        return generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_email_or_id(cls, search, value):
        """Checks if the database has email or id and returns it"""
        if search == 'email':
            return cls.query.filter_by(email=value).first()
        else:
            return cls.query.filter_by(id=value).first()
