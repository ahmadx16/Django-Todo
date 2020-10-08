import re
from .exceptions import InvalidTask


def validate_task(task_detail):
    invalid_task_characters = re.compile(r"[!@#$%^&*]")
    if invalid_task_characters.search(task_detail) or len(task_detail.strip()) == 0:
        raise InvalidTask("Task is either empty or contains invalid characters")


def get_tasks_errors(task_details):
    """ Validates tasks list and returns errors"""
    try:
        [validate_task(task) for task in task_details]
        return None
    except InvalidTask as error:
        return error
