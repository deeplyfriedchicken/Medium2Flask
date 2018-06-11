import schedule
import time
from flask import Flask
from db import db

from actions.feed import FeedScraper
from secrets import DB_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH


def job():
    medium = FeedScraper('https://medium.com/feed/')
    medium.getPosts()

with app.app_context():
    db.init_app(app)
    # run once to be sure
    job()
    # schedule cron for every 5 minutes
    schedule.every(5).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)