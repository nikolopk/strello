from django.shortcuts import render
from .models import Article


def index(request):
    all_articles = Article.objects.all()
    print all_articles[0].title
    context = {'all_articles': all_articles}
    return render(request, 'newsfeed/index.html', context)


def single_article(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article': article}
    return render(request, 'newsfeed/single_article.html', context)
