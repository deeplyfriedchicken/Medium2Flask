import requests, json, urllib.parse
from datetime import datetime

from models.blog import PostModel, CategoryModel

from models.account import AccountModel


class FeedScraper():
    """Scrapes the Medium XML and saves it to the DB"""
    def __init__(self, url):
        self.url = url

    def getPosts(self):
        accounts = AccountModel.find_all()
        urls = [(self.url + account.name) for account in accounts]
        i = 0
        for url in urls:
            print('Pulling posts from {}...'.format(url))
            
            rss = 'https://api.rss2json.com/v1/api.json?rss_url={}'.format(urllib.parse.quote_plus(url))
            data = requests.get(rss).json()

            print('====== ' + data['status'] + ' ======')

            for item in data['items']:
                pub_date = datetime.strptime(item['pubDate'], '%Y-%m-%d %H:%M:%S')
                # if exists, do not save unless pubDate is different
                post = PostModel.find_by_title(item['title'])
                categories = [CategoryModel.get_or_create(category) for category in item['categories']]
                new_post = PostModel(
                        accounts[i].id,
                        item['title'],
                        pub_date,
                        item['link'],
                        item['author'],
                        item['thumbnail'],
                        item['description'],
                        categories
                    )
                if post is None:
                    # add new
                    new_post.save_to_db()
                else:
                    if pub_date != post.pub_date:
                        # delete old
                        post.delete_from_db()
                        new_post.save_to_db()

            i += 1