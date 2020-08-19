from django.db import models


class Task(models.Model):
    """ Model for saving Tasks
    """
    detail = models.CharField(max_length=1000)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.detail
