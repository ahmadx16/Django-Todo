from django.urls import path
from .views import LoginView, SignupView, ProfileView, logout_request, server_exception

app_name = 'users'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('logout', logout_request, name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),

    # For server exception testing
    path('server-exception', server_exception, name='server-exception'),

]
