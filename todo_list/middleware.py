
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model


User = get_user_model()


class SessionAuthentication:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # adds user object to request if session key is in cookies

        request.user = AnonymousUser()
        session_key = request.COOKIES.get('sessionid',)
        if session_key:
            try:
                session = Session.objects.get(session_key=session_key)
                uid = session.get_decoded().get('_auth_user_id')
                user = User.objects.get(pk=uid)
                request.user = user
            except (User.DoesNotExist, Session.DoesNotExist):
                request.user = AnonymousUser()

        response = self.get_response(request)

        return response
