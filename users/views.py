from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth import get_user_model

from users.decorators import authenticated_user
from .forms.login_form import LoginForm
from .forms.signup_form import SignupForm
from .forms.profile_form import ProfileForm
from .utils import login_authenticate


User = get_user_model()

# Custom Error pages


def error_404_view(request, exception):
    return render(request, '404page.html')


def error_500_view(request):
    return render(request, '500page.html')


def logout_request(request):
    logout(request)
    return redirect('users:login')


class UserCreate(View):
    """ This is  just to test and learn update or create method"""
    
    @authenticated_user(view_type="class")
    def get(self, request):
        return render(request, 'users/create.html')

    @authenticated_user(view_type="class")
    def post(self, request):
        defaults = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
        }
        User.objects.update_or_create(email=request.POST.get('email'), defaults=defaults)
        return redirect('users:login')


class ProfileView(View):

    @authenticated_user(view_type="class")
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/")

        user = User.objects.select_related('profile').get(email=request.user.email)

        initial_form_values = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth': user.profile.date_of_birth,
            'bio': user.profile.bio,
        }

        form = ProfileForm(initial=initial_form_values)
        context = {
            "form": form
        }
        return render(request, 'users/profile.html', context)

    @authenticated_user(view_type="class")
    def post(self, request):
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('users:profile')


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tasks:task-view')

        login_form = LoginForm()
        context = {
            "form": login_form
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        form = LoginForm(data=request.POST)

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
