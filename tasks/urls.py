from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # /tasks/
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('update/<int:task_id>', views.update_task, name='update-task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete-task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle-task-complete'),
]
