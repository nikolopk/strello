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
from random import randint


def index(request):
    cache.clear()
    # latestArticleId = Article.objects.all().aggregate(Max('articleId'))
    user = request.user
    all_articles = []

    if user.is_authenticated():
        dbArticles = Article.objects.all()

        filename = str(user) + '.csv'
        fToWrite = open(filename, "wb")
        writer = csv.writer(fToWrite, delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_NONE,
                            escapechar='\\')
        writer.writerow(['id', 'title'])
        writer = csv.writer(fToWrite, delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_NONNUMERIC,
                            escapechar='\\')
        for article in dbArticles:
            _id = article.articleId
            _title = article.title
            writer.writerow([_id, _title.encode('utf-8')])
        fToWrite.close()
        fToWrite = open(filename, "rb")
        row_count = sum(1 for row in fToWrite)
        fToWrite.close()
        print 'csv rows: ' + str(row_count)

        randomIds = []
        for i in range(0, 5):
            randomIds.append(randint(1, row_count-1))
        print 'random ids:' + str(randomIds)

        content_engine = ContentEngine()
        ds = content_engine(filename)
        rec_table = content_engine._train(ds)

        for i in range(0, 5):
            table_to_return = content_engine.predict(randomIds[i], rec_table)
            print 'table to return: ' + str(table_to_return)
            all_articles.append(Article.objects.get(articleId=randomIds[i]))
            for recommended_article in table_to_return:
                if recommended_article in all_articles:
                    continue
                all_articles.append(Article.objects.get(articleId=recommended_article))

    context = {'all_articles': all_articles, 'user': user}
    return render(request, 'newsfeed/index.html', context)


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
