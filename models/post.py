import sqlite3
from db import db


class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(80))
    title = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime)
    link = db.Column(db.String(300))
    author = db.Column(db.String(80))
    thumbnail = db.Column(db.String(300))
    description = db.Column(db.Text)
    

    def __init__(self, account, title, pub_date, link, author, thumbnail, description):
        self.account = account
        self.title = title
        self.pub_date = pub_date
        self.link = link
        self.author = author
        self.thumbnail = thumbnail
        self.description = description
        #channel

    def json(self):
        return {
            'id': self.id,
            'account': self.account,
            'title': self.title,
            'publication_date': self.pub_date.__str__(),
            'link': self.link,
            'author': self.author,
            'thumbnail': self.thumbnail,
            'description': self.description
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
