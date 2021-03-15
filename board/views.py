from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article, Tag
import re


def index(request):
    article_list = Article.objects.all()
    return render(request, 'board/index.html', {
        'article_list': article_list,
    })


@login_required
def article_new(request):

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            tag_set = form.cleaned_data.get('tag_set')

            article = Article.objects.create(
                author=request.user, title=title, content=content)

            tag_name_list = re.findall(r'#([a-zA-Z\dㄱ-힣_+-]+)', tag_set)
            for tag_name in tag_name_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                article.tag_set.add(tag)

            return redirect(article)
    else:
        form = ArticleForm()

    return render(request, 'board/article_form.html', {
        'form': form,
    })


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'board/article_detail.html', {
        'article': article,
    })


@login_required
def article_edit(request, pk):

    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user:
        return HttpResponse(status=401)

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            article.save()

            new_tag_set = form.cleaned_data.get('tag_set')
            new_tag_name_list = re.findall(
                r'#([a-zA-Z\dㄱ-힣_+-]+)', new_tag_set)
            # Remove deleted tags
            for tag in article.tag_set.all():
                if tag.name not in new_tag_name_list:
                    article.tag_set.remove(tag)
            # Add new tags
            for tag_name in new_tag_name_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                article.tag_set.add(tag)

            return redirect(article)
    else:
        data = {
            'title': article.title,
            'content': article.content,
            'tag_set': article.tag_set_as_string(),
        }
        form = ArticleForm(data)

    return render(request, 'board/article_form.html', {
        'form': form,
    })


@login_required
def article_delete(request, pk):

    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user:
        return HttpResponse(status=401)

    article.delete()
    return redirect('board:index')
