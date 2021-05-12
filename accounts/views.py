from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from .forms import SignupForm, ProfileForm
from codus.helpers import get_page_range


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            login(request, signed_user)
            return redirect('board:index')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {
        'form': form
    })


login_view = LoginView.as_view(template_name='accounts/login_form.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('board:index')


@login_required
def profile(request):

    user = request.user
    scrap_set = user.scrap.article_set.all()[:5]
    article_set = user.article_set.all()[:5]
    comment_set = user.comment_set.all().order_by('-id')[:5]

    return render(request, 'accounts/profile.html', {
        'scrap_set': scrap_set,
        'article_set': article_set,
        'comment_set': comment_set,
    })


@login_required
def profile_edit(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile_form.html', {
        'form': form,
    })


@login_required
def myscraps(request):

    article_list = request.user.scrap.article_set.all()
    paginator = Paginator(article_list, 10)

    page_obj = paginator.get_page(request.GET.get('page', 1))
    page_number = page_obj.number
    page_range = get_page_range(paginator, page_number)

    return render(request, 'board/index.html', {
        'title': 'My Scraps',
        'page_obj': page_obj,
        'page_range': page_range,
    })


@login_required
def myarticles(request):

    article_list = request.user.article_set.all()
    paginator = Paginator(article_list, 10)

    page_obj = paginator.get_page(request.GET.get('page', 1))
    page_number = page_obj.number
    page_range = get_page_range(paginator, page_number)

    return render(request, 'board/index.html', {
        'title': 'My Articles',
        'page_obj': page_obj,
        'page_range': page_range,
    })
