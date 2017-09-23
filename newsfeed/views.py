#  -*- coding: utf-8 -*-
from .models import Article
from newsfeed.forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.cache import cache
from django.http import HttpResponseRedirect
import feedparser


def index(request):
    cache.clear()

    all_articles = []

    user = request.user
    rss = 'http://www2.zougla.gr/articlerss.xml'
    rss2 = 'http://rss.cnn.com/rss/edition_world.rss'
    rss3 = 'http://news247.gr/eidiseis/politiki/?widget=rssfeed&view=feed&contentId=5328'
    rss4 = 'http://feeds.bbci.co.uk/news/rss.xml'
    rss5 = 'http://feeds.reuters.com/reuters/businessNews'
    rss6 = 'http://www.dailymail.co.uk/articles.rss'
    rssUrl = feedparser.parse(rss6)

    for post in rssUrl.entries:
        _title = post.title
        _text = post.description
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
        all_articles.append(Article(title=_title,
                                    text=_text,
                                    link=_link,
                                    thumbnail = _thumbnail))

    # if user.is_authenticated():
    #     rssToProcess = user.rss
    #     for rss in rssToProcess:
    #         try:
    #             rssUrl = feedparser.parse(rss)
    #             for post in rssUrl.entries:
    #                 # print '\n'
    #                 # print 'Title: ' + post.title.encode('utf-8')
    #                 # print post.description.encode('utf-8')
    #                 # print post.link
    #                 # print post.media_thumbnail[0]['url']
    #                 # print '\n'
    #                 all_articles.append(Article(title = post.title, text = post.description, link = post.link, thumbnail = post.media_thumbnail[0]['url']))
    #         except:
    #             pass

    # all_articles = Article.objects.all()
    context = {'all_articles': all_articles, 'user': user}
    return render(request, 'newsfeed/index.html', context)


def prepend_ns(s):
    return '{http://www.w3.org/2005/Atom}' + s


def single_article(request, article_id):
    user = request.user
    if user.is_authenticated():
        article = Article.objects.get(id=article_id)
        user = request.user
        context = {'article': article, 'user': user}
        return render(request, 'newsfeed/single_article.html', context)
    else:
        return HttpResponseRedirect('/newsfeed')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/newsfeed')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'newsfeed/reg_form.html', args)


def logout_view(request):
    logout(request)
    return redirect('/newsfeed')


def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'newsfeed/profile.html', context)


def pref_change(request):
    if request.method == 'POST':
        worldPoints = request.POST.get('worldPoints')
        techPoints = request.POST.get('techPoints')
        sportsPoints = request.POST.get('sportsPoints')

        user = request.user
        user.worldPref = worldPoints
        user.techPref = techPoints
        user.sportsPref = sportsPoints
        user.save()

    return redirect('/newsfeed')


def add_rss(request):
    if request.method == 'POST':
        rssToAdd = request.POST.get('rss')

        user = request.user
        rssList = user.rss
        rssList.append(rssToAdd)
        user.rss = rssList
        user.save()

    return redirect('/newsfeed')
