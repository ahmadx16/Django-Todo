from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import User

from .forms.login_form import LoginForm
from .forms.signup_form import SignupForm
from .forms.profile_form import ProfileForm


def logout_request(request):
    logout(request)
    print("User logged out successfully")
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
        profile_form = ProfileForm(request.POST or None)
        if profile_form.is_valid():
            profile_form.save(request)

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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
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
            messages.error(request, "Invalid Form data. Please enter validform data")
            return redirect('users:signup')

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

        
            
