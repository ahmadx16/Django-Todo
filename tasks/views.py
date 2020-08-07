from django.shortcuts import render
from .models import Task


def index(request):
    # adding new tasks
    if request.method =='POST':
        task = Task (detail=request.POST['newtask'])
        task.save()
    
    all_tasks = Task.objects.all()
    context = {
        "all_tasks": all_tasks
    }

    
        
    return render(request, 'tasks/index.html',context)
