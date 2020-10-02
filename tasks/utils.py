import re
from .exceptions import InvalidTask


def validate_task(task_detail):
    invalid_task_characters = re.compile(r"[!@#$%^&*]")
    if invalid_task_characters.search(task_detail):
        raise InvalidTask("Invalid characters found in task")
