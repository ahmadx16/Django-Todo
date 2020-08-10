from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def index(request):
    # adding new tasks
    if request.method == 'POST':

        task = Task(detail=request.POST['newtask'])
        task.save()

    all_tasks = Task.objects.all()
    context = {
        "all_tasks": all_tasks
    }

    return render(request, 'tasks/index.html', context)


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("tasks:index")


def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_complete = not task.is_complete
    task.save()
    return redirect("tasks:index")