# -*- coding: utf-8 -*-
"""
    Models for database scheme.
"""
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager


class Article(models.Model):
    """ Model for each article. """
    articleId = models.IntegerField()
    title = models.CharField(max_length=250)
    description = models.TextField()
    link = models.TextField()
    thumbnail = models.TextField()
    timestamp = models.DateTimeField()


class RateArticle(models.Model):
    """ Stores rates of users for articles. """
    articleId = models.IntegerField()
    userId = models.CharField(max_length=100)
    rating = models.IntegerField()
    ratingMode = models.CharField(max_length=15)


class UserProfile(AbstractBaseUser):
    """ Stores users info """
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    gender = models.IntegerField()
    age_group = models.IntegerField()
    worldPref = models.PositiveSmallIntegerField(default=2)
    businessPref = models.PositiveSmallIntegerField(default=2)
    technologyPref = models.PositiveSmallIntegerField(default=2)
    sciencePref = models.PositiveSmallIntegerField(default=2)
    healthPref = models.PositiveSmallIntegerField(default=2)
    sportsPref = models.PositiveSmallIntegerField(default=2)
    politicsPref = models.PositiveSmallIntegerField(default=2)
    preferencesEnabled = models.BooleanField(default=False)
    ratingsEnabled = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = u'newsfeed_userprofile'
