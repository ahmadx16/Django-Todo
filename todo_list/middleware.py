
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser
from users.models import CustomUser


class CustomAuthentication:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # adds user object to request if session key in cookies

        session_key = request.COOKIES.get('sessionid',)
        if session_key:
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = CustomUser.objects.get(pk=uid)
            request.user = user
        else:
            request.user = AnonymousUser()
        response = self.get_response(request)

        return response
