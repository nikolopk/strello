from django.shortcuts import render
from .models import Article


def index(request):
    all_articles = Article.objects.all()
    context = {'all_articles': all_articles}
    return render(request, 'newsfeed/index.html', context)
