from django.shortcuts import redirect
from django.contrib.auth import authenticate, login


def login_authenticate(request, form_data):
    print(form_data)
    email = form_data.get('email')
    password = form_data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)

        return True
    return False
