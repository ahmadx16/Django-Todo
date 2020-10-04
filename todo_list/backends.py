from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


User = get_user_model()


class CustomBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            pwd_valid = check_password(password, user.password)
            if not pwd_valid:
                return None

            return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
