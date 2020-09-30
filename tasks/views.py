from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Task


def index(request):
    """View all tasks"""
    
    all_tasks = {}
    if request.user.is_authenticated:
        all_tasks = request.user.task_set.all()
    context = {
        "all_tasks": all_tasks
    }

    return render(request, 'tasks/index.html', context)

def toggle_task(request):
    """Toggle complete or incomplete of given id"""

    if request.method == 'POST':
        task_id = request.POST['task_id']
        task = get_object_or_404(Task, id=task_id)
        task.is_complete = not task.is_complete
        task.save()
        return redirect("tasks:index")


def update_form(request, task_id):
    """Makes available update form for selected task """

    all_tasks = {}
    if request.user.is_authenticated:
        all_tasks = request.user.task_set.all()
    context = {
        "all_tasks": all_tasks,
        "edit_task": task_id
    }

    return render(request, 'tasks/index.html', context)


class TaskView(View):

    def get(self, request):
        all_tasks = {}
        if request.user.is_authenticated:
            all_tasks = request.user.task_set.all()
        context = {
            "all_tasks": all_tasks
        }
        return render(request, 'tasks/index.html', context)

    def post(self, request):

        method = request.POST.get('method', 0)
        # add new task
        if method == 'POST':
            task = Task(user=request.user, detail=request.POST['task_detail'])
            task.save()
            return redirect("tasks:task-view")

        # update task detail
        elif method == 'PUT':
            task_id = request.POST['task_id']
            task = get_object_or_404(Task, id=task_id)
            task.detail = request.POST['task_detail']
            task.save()
            return redirect("tasks:task-view")

        # deleting a task
        elif method == 'DELETE':
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id)
            task.delete()
            return redirect("tasks:task-view")
