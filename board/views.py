from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .forms import ArticleForm, CommentForm
from .models import Article, Tag, Comment, Scrap
from codus.helpers import get_page_range
import re


def index(request):

    article_list = Article.objects.all()
    paginator = Paginator(article_list, 10)

    page_obj = paginator.get_page(request.GET.get('page', 1))
    page_number = page_obj.number
    page_range = get_page_range(paginator, page_number)

    return render(request, 'board/index.html', {
        'page_obj': page_obj,
        'page_range': page_range,
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
        redirect_url = request.META.get('HTTP_REFERER', '/')

    return render(request, 'board/article_form.html', {
        'form': form,
        'redirect_url': redirect_url,
    })


def article_detail(request, pk):

    user = request.user
    article = get_object_or_404(Article, pk=pk)
    comment_list = article.comment_set.all()
    comment_form = CommentForm()

    if user.is_authenticated:
        user_scrap = user.scrap
        is_scrapped = user_scrap.article_set.filter(id=article.pk).exists()
    else:
        is_scrapped = None

    return render(request, 'board/article_detail.html', {
        'article': article,
        'comment_list': comment_list,
        'comment_form': comment_form,
        'is_scrapped': is_scrapped,
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
        redirect_url = article.get_absolute_url()

    return render(request, 'board/article_form.html', {
        'form': form,
        'redirect_url': redirect_url,
    })


@login_required
def article_delete(request, pk):

    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user:
        return HttpResponse(status=401)

    article.delete()
    return redirect('board:index')


@csrf_exempt
@login_required
def article_scrap(request, pk):

    article = get_object_or_404(Article, pk=pk)
    user = request.user

    if request.method == 'POST':

        scrap, created = Scrap.objects.get_or_create(user=user)
        scrap.article_set.add(article)

        return JsonResponse({'status': True})

    return JsonResponse({'status': False})


@csrf_exempt
@login_required
def article_unscrap(request, pk):

    article = get_object_or_404(Article, pk=pk)
    user = request.user

    if request.method == 'PUT':

        user_scrap = user.scrap
        user_scrap.article_set.remove(article)
        return JsonResponse({'status': True})

    return JsonResponse({'status': False})


@login_required
def comment_new(request, article_pk):

    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()

    return redirect(article)


@login_required
def comment_edit(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponse(status=401)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect(comment.article)

    return redirect(comment.article)


@login_required
def comment_delete(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponse(status=401)

    comment.delete()
    return HttpResponse(status=200)
