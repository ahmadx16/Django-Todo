from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def index(request):
    """View all tasks"""

    all_tasks = Task.objects.all()
    context = {
        "all_tasks": all_tasks
    }

    return render(request, 'tasks/index.html', context)


def add(request):
    """Adding new tasks"""

    if request.method == 'POST':
        task = Task(detail=request.POST['newtask'])
        task.save()
    return redirect("tasks:index")


def delete_task(request, task_id):
    """Delete task on given task_id"""

    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("tasks:index")


def toggle_task(request, task_id):
    """Toggle complete or incomplete of given id"""

    task = get_object_or_404(Task, id=task_id)
    task.is_complete = not task.is_complete
    task.save()
    return redirect("tasks:index")


def update_task(request, task_id):
    """Updates taskof given task_id"""

    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.detail = request.POST['updated_task']
        task.save()
        return redirect("tasks:index")

    all_tasks = Task.objects.all()
    context = {
        "all_tasks": all_tasks,
        "edit_task": task_id
    }

    return render(request, 'tasks/index.html', context)
