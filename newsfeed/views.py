from .models import Article
from newsfeed.forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def welcome_screen(request):
    context = {}
    return render(request, 'newsfeed/welcome_screen.html', context)


def index(request):
    all_articles = Article.objects.all()
    user = request.user
    context = {'all_articles': all_articles, 'user': user}
    return render(request, 'newsfeed/index.html', context)


def single_article(request, article_id):
    article = Article.objects.get(id=article_id)
    user = request.user
    context = {'article': article, 'user': user}
    return render(request, 'newsfeed/single_article.html', context)


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
