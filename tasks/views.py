from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages

from .models import Task
from .exceptions import InvalidTask
from .utils import validate_task


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
    http_method_names = ['get', 'post', 'put', 'delete']

    # handle put and delete for html forms
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(TaskView, self).dispatch(*args, **kwargs)

    def get(self, request):
        all_tasks = {}
        if request.user.is_authenticated:
            all_tasks = request.user.task_set.all()
        context = {
            "all_tasks": all_tasks
        }
        return render(request, 'tasks/index.html', context)

    def post(self, request):
        # add new task

        try:
            task_detail = request.POST['task_detail']
            validate_task(task_detail)
            task = Task(user=request.user, detail=task_detail)
            task.save()
            return redirect("tasks:task-view")
        except InvalidTask:
            messages.error(request, "Invalid Task: Cannot add task. Make  sure your task contains valid characters")
            return redirect("tasks:task-view")

        
    def put(self, request):
        task_id = request.POST['task_id']
        task = get_object_or_404(Task, id=task_id)
        task.detail = request.POST['task_detail']
        task.save()
        return redirect("tasks:task-view")

    def delete(self, request):
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return redirect("tasks:task-view")
