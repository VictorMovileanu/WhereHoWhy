from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from main.forms import TweetForm
from main.models import Tweet


def quotes(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
    else:
        form = TweetForm()

    tweets = Tweet.objects.all()
    return render(request, 'frontpage/quotes.html', {'form': form, 'tweets': tweets})


def knowledge_tree(request):
    return TemplateResponse(request, 'frontpage/knowledge_tree.html')
