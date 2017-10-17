#  -*- coding: utf-8 -*-
from newsfeed.models import Article
from newsfeed.models import RateArticle
from newsfeed.forms import RegistrationForm
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.core.cache import cache
from django.http import HttpResponseRedirect
import feedparser
from ContentEngine import ContentEngine
import csv
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q


def index(request):
    cache.clear()
    Article.objects.all().delete()
    # latestArticleId = Article.objects.all().aggregate(Max('articleId'))
    user = request.user

    all_articles = []
    filename = str(user) + '.csv'
    fToWrite = open(filename, "wb")
    writer = csv.writer(fToWrite, delimiter=';',
                        quotechar='"',
                        quoting=csv.QUOTE_NONE,
                        escapechar='\\')
    writer.writerow(['id', 'title', 'description'])
    writer = csv.writer(fToWrite, delimiter=';',
                        quotechar='"',
                        quoting=csv.QUOTE_NONNUMERIC,
                        escapechar='\\')

    rss = 'http://www2.zougla.gr/articlerss.xml'
    rss2 = 'http://rss.cnn.com/rss/edition_world.rss'
    rss3 = 'http://news247.gr/eidiseis/politiki/?widget=rssfeed&view=feed&contentId=5328'
    rss4 = 'http://feeds.bbci.co.uk/news/rss.xml'
    rss5 = 'http://feeds.reuters.com/reuters/businessNews'
    rss6 = 'http://www.dailymail.co.uk/articles.rss'
    rss7 = 'https://www.newsinlevels.com/feed/'
    rssUrl = feedparser.parse(rss6)

    postId = 1
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
        writer.writerow([postId, _title.encode('utf-8'), _description.encode('utf-8')])
        tempArticle = Article(articleId=postId,
                              title=_title,
                              description=_description,
                              link=_link,
                              thumbnail=_thumbnail)
        tempArticle.save()
        postId += 1
    fToWrite.close()

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

    # content_engine = ContentEngine()
    # ds = content_engine(filename)
    # rec_table = content_engine._train(ds)
    # table_to_return = content_engine.predict(6, rec_table)

    all_articles.append(Article.objects.get(articleId=6))
    all_articles.append(Article.objects.get(articleId=10))
    # for recommended_article in table_to_return:
    #     all_articles.append(Article.objects.get(articleId=recommended_article))

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
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/newsfeed')
        else:
            args = {'form': form}
            return render(request, 'newsfeed/reg_form.html', args)
    else:
        # form = UserCreationForm()
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
        businessPoints = request.POST.get('businessPoints')
        technologyPoints = request.POST.get('technologyPoints')
        sciencePoints = request.POST.get('sciencePoints')
        healthPoints = request.POST.get('healthPoints')
        sportsPoints = request.POST.get('sportsPoints')
        politicsPoints = request.POST.get('politicsPoints')

        user = request.user
        user.worldPref = worldPoints
        user.businessPref = businessPoints
        user.technologyPref = technologyPoints
        user.sciencePref = sciencePoints
        user.healthPref = healthPoints
        user.sportsPref = sportsPoints
        user.politicsPref = politicsPoints
        user.save()

    return redirect('/newsfeed')


def save_ratings(request):
    print 'In save settings'
    queryCheck = 0
    if request.is_ajax():
        requestId = request.POST.get('id')
        requestValue = request.POST.get('value')
        user = request.user
        print 'id:' + requestId + ' value:' + requestValue
        print 'user id:' + user.id
        queryCheck = RateArticle.objects.filter(userId=user.id, articleId=requestId).update(rating=requestValue)
        print str(queryCheck)

        # for query in queryset:
        #     queryCheck = query.userId
        if queryCheck == 0:
            tempRate = RateArticle(articleId=requestId, userId=user.id, rating=requestValue)
            tempRate.save()


def add_rss(request):
    if request.method == 'POST':
        rssToAdd = request.POST.get('rss')

        user = request.user
        rssList = user.rss
        rssList.append(rssToAdd)
        user.rss = rssList
        user.save()

    return redirect('/newsfeed')
