from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm


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
