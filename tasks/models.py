from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """ Model for saving Tasks
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    detail = models.CharField(max_length=1000)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.detail
