# -*- coding: utf-8 -*-
""" Script for updating the database """
import feedparser
import datetime
from pymongo import MongoClient

client = MongoClient()
db = client.strello_db
articles = db.newsfeed_article

try:
    last_articles = articles.find({}).sort("_id", -1).limit(1)
    last_id = 0
    for doc in last_articles:
        last_id = doc['articleId']
    post_id = last_id + 1

    rss_list = ['http://feeds.bbci.co.uk/news/world/rss.xml']
               # 'http://feeds.bbci.co.uk/news/business/rss.xml',
               # 'http://feeds.bbci.co.uk/news/politics/rss.xml',
               # 'http://feeds.bbci.co.uk/news/health/rss.xml',
               # 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
               # 'http://feeds.bbci.co.uk/news/technology/rss.xml',
               # 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
               # 'http://feeds.bbci.co.uk/news/education/rss.xml',
               # 'http://www.dailymail.co.uk/articles.rss',
               # 'https://api.foxsports.com/v1/rss?partnerKey=zBaFxRyGKCfxBagJG9b8pqLyndmvo7UU&tag=soccer',
               # 'https://www.cbsnews.com/latest/rss/us',
               # 'https://www.cbsnews.com/latest/rss/world',
               # 'https://www.cbsnews.com/latest/rss/health',
               # 'https://www.cbsnews.com/latest/rss/entertainment',
               # 'https://www.cbsnews.com/latest/rss/moneywatch',
               # 'https://www.cbsnews.com/latest/rss/tech',
               # 'https://www.cbsnews.com/latest/rss/politics']

    # rssList = ['http://rss.cnn.com/rss/edition_world.rss']
    # rssList = ['http://feeds.reuters.com/reuters/businessNews']
    # rssList = ['https://www.newsinlevels.com/feed/']
    # rssList = ['']
    for rss_url in rss_list:
        rss_to_parse = feedparser.parse(rss_url)
        for post in rss_to_parse.entries:
            _title = post.title
            _description = post.description
            _link = post.link
            _thumbnail = 'http://ccwc.org/wp-content/themes/ccwc-theme/images/no-image-available.png'
            try:
                _thumbnail = post.media_thumbnail[0]['url']
            except:
                pass

            try:
                _thumbnail = post.enclosures[0].href
            except:
                pass

            existing_link = articles.find_one({"link": _link})
            if existing_link is None:
                result = articles.insert_one(
                    {
                        "articleId": post_id,
                        "title": _title,
                        "description": _description,
                        "link": _link,
                        "thumbnail": _thumbnail,
                        "timestamp": datetime.datetime.utcnow()
                    }
                )
                post_id += 1

except Exception as ex:
    print ex
    pass
