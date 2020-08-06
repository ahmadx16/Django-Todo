from django.db import models


class Task(models.Model):
    """ Model for saving Tasks
    """
    details = models.CharField(max_length=500),
    iscomplete = models.BooleanField(default=False)

