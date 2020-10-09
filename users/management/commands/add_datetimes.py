import datetime as dt
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from users.models import DateTime, ConvertDateTo

User = get_user_model()


class Command(BaseCommand):
    help = 'Add 100 datetimes'

    def handle(self, *args, **options):

        for _ in range(100):
            # adds 100 PST (UTC+5) datetimes in databases
            DateTime(datetime=dt.datetime.utcnow() + dt.timedelta(hours=5), region="PST").save()
        
        ConvertDateTo(convert_to="UTC").save()
