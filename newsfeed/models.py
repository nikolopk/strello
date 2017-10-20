# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from djangotoolbox.fields import ListField


class Article(models.Model):
    articleId = models.IntegerField()
    title = models.CharField(max_length=250)
    description = models.TextField()
    link = models.CharField(max_length=2000)
    thumbnail = models.CharField(max_length=2000)
    timestamp = models.DateTimeField()


class RateArticle(models.Model):
    articleId = models.IntegerField()
    userId = models.CharField(max_length=100)
    rating = models.IntegerField()


class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    worldPref = models.PositiveSmallIntegerField(default=2)
    businessPref = models.PositiveSmallIntegerField(default=2)
    technologyPref = models.PositiveSmallIntegerField(default=2)
    sciencePref = models.PositiveSmallIntegerField(default=2)
    healthPref = models.PositiveSmallIntegerField(default=2)
    sportsPref = models.PositiveSmallIntegerField(default=2)
    politicsPref = models.PositiveSmallIntegerField(default=2)
    cfEnabled = models.BooleanField(default=False)
    # rss = ListField(models.CharField(max_length=2000), default=[])
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = u'newsfeed_userprofile'