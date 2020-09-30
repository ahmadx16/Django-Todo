from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from .forms.login_form import LoginForm
from .forms.signup_form import SignupForm


def logout_request(request):
    logout(request)
    print("User logged out successfully")
    return redirect('users:login')


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tasks:task-view')

        login_form = AuthenticationForm()
        context = {
            "form": login_form
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"You are now logged in as {username}")
                return redirect('/')
            else:
                print("Invalid username or password.")
        else:
            print("Invalid username or password.")

        return redirect('users:login')


class SignupView(View):

    def get(self, request, error_messages=None):
        if request.user.is_authenticated:
            return redirect('tasks:task-view')

        signup_form = SignupForm()
        context = {
            "form": signup_form,
            "error_messages": error_messages
        }
        return render(request, "users/signup.html", context)

    def post(self, request):
        signup_form = SignupForm(request.POST or None)
        if signup_form.is_valid():
            signup_form.save()

            # auto login after signup
            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"You are now logged in as {username}")
                return redirect('/')

            return redirect('users:signup')
