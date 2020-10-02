from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth.models import User

from .forms.login_form import LoginForm
from .forms.signup_form import SignupForm
from .forms.profile_form import ProfileForm
from .utils import login_authenticate


# Custom Error pages
def error_404_view(request, exception):
    return render(request, '404page.html')


def error_500_view(request):
    return render(request, '500page.html')


def logout_request(request):
    logout(request)
    return redirect('users:login')


class ProfileView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/")

        initial_form_values = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'date_of_birth': request.user.profile.date_of_birth,
            'bio': request.user.profile.bio,
        }

        form = ProfileForm(initial=initial_form_values)
        context = {
            "form": form
        }
        return render(request, 'users/profile.html', context)

    def post(self, request):
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('users:profile')


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
            if login_authenticate(request, form.cleaned_data):
                return redirect('/')

        messages.error(request, "Invalid username or password.")
        return redirect('users:login')


class SignupView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tasks:task-view')

        signup_form = SignupForm()
        context = {
            "form": signup_form,
        }
        return render(request, "users/signup.html", context)

    def post(self, request):
        signup_form = SignupForm(request.POST or None)

        # return when invalid form data
        if not signup_form.is_valid():
            messages.error(request, "Invalid Form data. Please enter valid form data")
            return redirect('users:signup')

        signup_form.save()

        # auto login after signup
        if login_authenticate(request, signup_form.cleaned_data):
            return redirect('/')

        return redirect('users:signup')
