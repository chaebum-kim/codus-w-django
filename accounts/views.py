from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import SignupForm, ProfileForm


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
def profile_edit(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_edit')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile_form.html', {
        'form': form,
    })
