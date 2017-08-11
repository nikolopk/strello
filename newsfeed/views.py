from .models import Article
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index(request):
    all_articles = Article.objects.all()
    context = {'all_articles': all_articles}
    return render(request, 'newsfeed/index.html', context)


def single_article(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article': article}
    return render(request, 'newsfeed/single_article.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print 'post'
        if form.is_valid():
            form.save()
            return redirect('/newsfeed')
    else:
        print 'get'
        form = UserCreationForm()
        args = {'form': form}
        return render(request, 'newsfeed/reg_form.html', args)
