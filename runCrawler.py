from bs4 import BeautifulSoup
from urlparse import urlparse
from pymongo import MongoClient
import urllib2

client = MongoClient()
db = client.rello_db

host = "http://www.bbc.com"
urlsParsed = []
urlsToGo = ["http://www.bbc.com/news/world-australia-40822310"]

try:
    while True:

        urlsToGo.reverse()
        url = urlsToGo.pop()
        print url

        try:
            content = urllib2.urlopen(url).read()
            urlsParsed.append(url)
            soup = BeautifulSoup(content, "lxml")

            try:
                title = soup.find("h1", {"class": "story-body__h1"})
                if title is not None:
                    title = title.getText()
                    print title

                    textToSave = ""
                    textDiv = soup.find("div", {"class": "story-body__inner"})
                    for par in textDiv.find_all('p'):
                        textToSave += par.getText()
                        print par.getText()

                    result = db.newsfeed_article.insert_one(
                        {
                            "title": title,
                            "text": textToSave
                        }
                    )

            except Exception as ex:
                print ex
                pass

            for links in soup.find_all('a'):
                try:
                    urlFind = links.get('href')

                    if not (urlFind.startswith('http://') or urlFind.startswith('https://')):
                        urlFind = host + urlFind

                    parsed_uri = urlparse(urlFind)
                    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                    domain = domain.rstrip('/')

                    urlFind = urlFind.rstrip('/')

                    if ((not ((urlFind in urlsParsed) or (urlFind in urlsToGo))) and (domain == host)):
                        urlsToGo.append(urlFind)
                except:
                    pass

        except Exception as ex:
            print ex
            pass

        if not urlsToGo:
            break
except Exception as ex:
    print ex
    pass

print (len(urlsParsed))

