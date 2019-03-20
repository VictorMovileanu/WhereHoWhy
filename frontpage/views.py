from django.shortcuts import render
from frontpage.forms import TweetForm
from frontpage.models import Tweet


def frontpage(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
    else:
        form = TweetForm()

    tweets = Tweet.objects.all()
    return render(request, 'frontpage/index.html', {'form': form, 'tweets': tweets})
