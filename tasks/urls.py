from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # /tasks/
    path('', views.index, name='index')
]
