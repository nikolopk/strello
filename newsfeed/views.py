#  -*- coding: utf-8 -*-
""" View file """
import csv
import datetime
import os
import json
from random import randint
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.cache import cache
from django.contrib.auth import login, authenticate
from newsfeed.models import Article
from newsfeed.models import RateArticle
from newsfeed.forms import RegistrationForm
from newsfeed.ContentEngine import ContentEngine
from newsfeed.NikoloEngine import NikoloEngine

def index(request):
    """ Initial method, responsible for serving to users articles"""
    cache.clear()
    user = request.user
    all_articles = []
    all_articles_ids = []
    wanted_ids = []

    try:
        if user.is_authenticated():
            today = datetime.datetime.utcnow()
            fixed_date = datetime.datetime.strptime(str(today), '%Y-%m-%d %H:%M:%S.%f')
            fixed_date_final = fixed_date - datetime.timedelta(days=2)
            db_articles = Article.objects.filter(timestamp__gte=fixed_date_final)

            filename = str(user) + '.csv'
            f_to_write = open(filename, "wb")
            writer = csv.writer(f_to_write, delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_NONE,
                                escapechar='\\')
            writer.writerow(['id', 'title'])
            writer = csv.writer(f_to_write, delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC,
                                escapechar='\\')
            for article in db_articles:
                _id = article.articleId
                _title = article.title
                writer.writerow([_id, _title.encode('utf-8')])
            f_to_write.close()

            user_objects = RateArticle.objects.filter(userId=user.id, rating__gte=1)
            if len(user_objects) > 10:
                user.ratingsEnabled = True
            else:
                user.ratingsEnabled = False

            if (not user.ratingsEnabled) or (not user.preferencesEnabled):
                f_to_write = open(filename, "rb")
                row_count = sum(1 for row in f_to_write)
                f_to_write.close()

                for i in range(0, 5):
                    wanted_ids.append(randint(1, row_count - 1))

            else:
                nikolo_engine = NikoloEngine()
                user_mongo_ids = nikolo_engine()
                similar_vector = nikolo_engine.train(user_mongo_ids)
                wanted_ids = nikolo_engine.predict(similar_vector,
                                                   user_mongo_ids,
                                                   user_mongo_ids.index(user.id))

            content_engine = ContentEngine()
            dataset = content_engine(filename)
            rec_table = ContentEngine._train(dataset)

            for i in range(0, len(wanted_ids)):
                table_to_return = ContentEngine.predict(wanted_ids[i], rec_table)
                all_articles_ids.append(wanted_ids[i])
                for recommended_article in table_to_return:
                    all_articles_ids.append(recommended_article)

            unique_articles_ids = list(set(all_articles_ids))
            for row in unique_articles_ids:
                all_articles.append(Article.objects.get(articleId=row))
            os.remove(filename)
    except Exception as ex:
        print ex
        pass
    context = {'all_articles': all_articles, 'user': user}
    return render(request, 'newsfeed/index.html', context)


def register(request):
    """ Handles the registration of the user """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

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
        form = RegistrationForm()
        args = {'form': form}
    return render(request, 'newsfeed/reg_form.html', args)


def logout_view(request):
    """ Handles the logout of the user """
    logout(request)
    return redirect('/newsfeed')


def profile(request):
    """ Display user profile page """
    user = request.user
    context = {'user': user}
    return render(request, 'newsfeed/profile.html', context)


def pref_change(request):
    """ Called if user save his new preferences - Stores new prefs in db """
    if request.method == 'POST':
        world_points = request.POST.get('worldPoints')
        business_points = request.POST.get('businessPoints')
        technology_points = request.POST.get('technologyPoints')
        science_points = request.POST.get('sciencePoints')
        health_points = request.POST.get('healthPoints')
        sports_points = request.POST.get('sportsPoints')
        politics_points = request.POST.get('politicsPoints')

        user = request.user
        user.worldPref = world_points
        user.businessPref = business_points
        user.technologyPref = technology_points
        user.sciencePref = science_points
        user.healthPref = health_points
        user.sportsPref = sports_points
        user.politicsPref = politics_points

        user.preferencesEnabled = True
        user.save()

    return redirect('/newsfeed')


def save_ratings(request):
    """ Stores in db the ratings of users for the articles """
    print 'In save settings'
    query_check = 0
    if request.is_ajax():
        request_id = request.POST.get('id')
        request_value = request.POST.get('value')

        user = request.user
        if user.ratingsEnabled and user.preferencesEnabled:
            rating_mode = 'NikoloEngine'
        else:
            rating_mode = 'ContentEngine'

        query_check = RateArticle.objects.filter(userId=user.id,
                                                 articleId=request_id).update(rating=request_value,
                                                                              ratingMode=rating_mode)

        if query_check == 0:
            temp_rate = RateArticle(articleId=request_id, userId=user.id, rating=request_value, ratingMode=rating_mode)
            temp_rate.save()
    response_dict = {'success': 'true'}
    return HttpResponse(json.dumps(response_dict), mimetype="application/json")
