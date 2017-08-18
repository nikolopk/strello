from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', login, {'template_name': 'newsfeed/login_form.html'}),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^prefChange/$', views.pref_change, name='pref_change'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^(?P<article_id>[-\w]+)/$', views.single_article, name='single_article'),
]

