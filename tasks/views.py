from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Task
from .exceptions import InvalidTask
from .utils import validate_task

User = get_user_model()


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

            user = User.objects.prefetch_related('task_set').get(email=request.user.email)
            all_tasks = user.task_set.all()
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

            # For model level validations check
            try:
                task.full_clean()
                _, created = Task.objects.get_or_create(user=request.user, detail=task_detail)
                if not created:
                    messages.error(request, "Task already exists")
                return redirect("tasks:task-view")
            except ValidationError as error:

                messages.error(request, error)
                return redirect("tasks:task-view")

        except InvalidTask as error:
            messages.error(request, error)
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


# Search Task View
def search_task(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    search_text = request.GET.get('search_text',)
    if search_text:
        query_tasks = request.user.task_set.filter(Q(detail__icontains=search_text))
    else:
        query_tasks = request.user.task_set.all()

    return render(request, 'tasks/search.html', context={'query_tasks': query_tasks})


# ----- Bulk Tasks Operations -----

def bulk_index(request):

    if not request.user.is_authenticated:
        return redirect('users:login')

    all_tasks = request.user.task_set.all()

    return render(request, 'tasks/bulk_operations.html', context={'all_tasks': all_tasks})


def bulk_add(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    if request.method == 'POST':
        task_details = request.POST.get('task_detail').split('\r')
        task_objs = [Task(user=request.user, detail=task_detail) for task_detail in task_details]
        Task.objects.bulk_create(task_objs)

    return redirect('tasks:bulk-index')


def bulk_update(request):

    if not request.user.is_authenticated:
        return redirect('users:login')

    if request.method == 'POST':
        task_ids = request.POST.getlist('task_id')
        task_details = request.POST.getlist('task_detail')
        task_objs = list(Task.objects.filter(pk__in=task_ids))

        for i in range(len(task_ids)):
            task_objs[i].detail = task_details[i]

        Task.objects.bulk_update(task_objs, ['detail'])

    return redirect('tasks:bulk-index')
