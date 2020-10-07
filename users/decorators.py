from django.shortcuts import redirect


def authenticated_user(view_type="func"):
    """ Lets only authenticates users to call view."""

    def authenticated_func(func):
        def authenticate(*args, **kwargs):

            request = args[0]
            if view_type == "class":
                request = args[1]

            if not request.user.is_authenticated:
                return redirect('users:login')

            return func(*args, **kwargs)

        return authenticate

    return authenticated_func
