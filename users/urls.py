from django.urls import path
from .views import LoginView, SignupView, ProfileView, logout_request

app_name = 'users'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('logout', logout_request, name='logout'),
    path('profile', ProfileView.as_view(), name='profile')

]
