from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # /tasks/
    path('', views.index, name='index'),
    path('update/<int:task_id>', views.update_form, name='update-form'),
    path('toggle/', views.toggle_task, name='toggle-task-complete'),
    path('search/', views.search_task, name='search-tasks'),

    # Bulk Tasks operations

    path('bulk', views.bulk_index, name='bulk-index'),
    path('bulk/add', views.bulk_add, name='bulk-add'),
    path('bulk/update', views.bulk_update, name='bulk-update'),
    

    # Class based views
    path('class', views.TaskView.as_view(), name='task-view')

]
