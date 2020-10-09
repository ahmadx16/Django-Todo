from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from users.models import DateTime, ConvertDateTo

User = get_user_model()


class Command(BaseCommand):
    help = 'Changes timezone of DataTime model'

    def get_swap_timezone(self, region):
        return "PST" if region == "UTC" else "UTC"

    def set_correct_region(self):
        """ Sets appropriate region to convert"""
        convert_date_obj = ConvertDateTo.objects.latest('id')
        datetimes = DateTime.objects.filter(region=self.get_swap_timezone(convert_date_obj.convert_to))

        # changes convert_to if all dates already converted
        if not datetimes.count():
            convert_date_obj.convert_to = self.get_swap_timezone(convert_date_obj.convert_to)
            convert_date_obj.save()

        return convert_date_obj.convert_to

    def convert_time(self, convert_to, date):
        """ Converts to PST by adding 5 hours when, subtracts in case of UTC"""

        if convert_to == "UTC":
            return date.datetime - timedelta(hours=5)
        return date.datetime + timedelta(hours=5)

    def handle(self, *args, **options):

        convert_to = self.set_correct_region()
        datetimes = DateTime.objects.filter(region=self.get_swap_timezone(convert_to))

        # convert 10 dates
        for date in datetimes[:10]:
            date.datetime = self.convert_time(convert_to, date)
            date.region = convert_to
            date.save()
