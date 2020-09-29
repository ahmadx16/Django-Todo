from django.shortcuts import render
from django.http import HttpResponse

from .forms.login_form import LoginForm
from .forms.signup_form import SignupForm

def login(request):
    login_form = LoginForm()
    context = {
        "form": login_form
    }
    return render(request, 'users/login.html', context)

def signup(request):
    signup_form = SignupForm()
    context = {
        "form": signup_form
    }
    return render(request, "users/signup.html", context)

