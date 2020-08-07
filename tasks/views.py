from django.shortcuts import render
from .models import Task


def index(request):
    all_tasks = Task.objects.all()
    context = {
        "all_tasks": all_tasks
    }
    return render(request, 'tasks/index.html',context)
