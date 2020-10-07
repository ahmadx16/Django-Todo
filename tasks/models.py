from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


def validate_detail(task_detail):
    if len(task_detail) == 0:
        raise ValidationError(
            _('%(value)s is not a valid task'),
            params={'value': task_detail},
        )


class Task(models.Model):
    """ Model for saving Tasks
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    detail = models.CharField(max_length=1000, validators=[validate_detail])
    is_complete = models.BooleanField(default=False)
    slug = models.SlugField(null=True, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.detail)
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.detail
