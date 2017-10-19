# -*- coding: utf-8 -*-
from pymongo import MongoClient
import feedparser
import datetime

client = MongoClient()
db = client.rello_db
articles = db.newsfeed_article

try:

    rss2 = 'http://rss.cnn.com/rss/edition_world.rss'
    rss4 = 'http://feeds.bbci.co.uk/news/rss.xml'
    rss5 = 'http://feeds.reuters.com/reuters/businessNews'
    rss6 = 'http://www.dailymail.co.uk/articles.rss'
    rss7 = 'https://www.newsinlevels.com/feed/'
    rssUrl = feedparser.parse(rss4)

    lastArticles = articles.find({}).sort("_id", -1).limit(1)
    lastId = 0
    for doc in lastArticles:
        lastId = doc['articleId']
    postId = lastId + 1

    # now = datetime.datetime.now()
    #date = now.strftime("%Y-%m-%d")
    for post in rssUrl.entries:
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

        existingLink = articles.find_one({"link": _link})
        if existingLink is None:
            result = articles.insert_one(
                {
                    "articleId": postId,
                    "title": _title,
                    "description": _description,
                    "link": _link,
                    "thumbnail": _thumbnail,
                    "date": datetime.datetime.utcnow()
                }
            )
            # print date
            postId += 1

except Exception as ex:
    print ex
    pass
