from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import CreateView

from frontpage.forms import TweetForm, PostForm, ProjectForm
from frontpage.models import Tweet, Post, Project


class HomeView(View):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return TemplateResponse(request, 'frontpage/index.html', context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('type') == "newProject":
            pass
        elif request.POST.get('type') == "newPost":
            pass
        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, request):
        ctx = dict()
        ctx['project_form'] = ProjectForm()
        ctx['post_form'] = PostForm()
        return ctx


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
