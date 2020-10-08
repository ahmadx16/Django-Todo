from django import template
from django.contrib.auth import get_user_model

from ..models import Task


register = template.Library()


@register.simple_tag
def all_tasks_count():
    return Task.objects.count()


@register.simple_tag
def all_users_count():
    return get_user_model().objects.count()
