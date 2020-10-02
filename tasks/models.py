from django.db import models
from django.conf import settings


class Task(models.Model):
    """ Model for saving Tasks
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    detail = models.CharField(max_length=1000)
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.detail
