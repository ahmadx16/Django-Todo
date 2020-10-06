from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a user given email and password'

    def add_arguments(self, parser):
        parser.add_argument('email', nargs=1, type=str)
        parser.add_argument('password', nargs=1, type=str)

    def handle(self, *args, **options):

        # creates user
        try:
            User.objects.create_user(email=options['email'][0], password=options['password'][0])
        except IntegrityError:
            self.stderr.write('User with the given email already exists')
