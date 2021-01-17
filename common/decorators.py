from django.http import HttpResponseRedirect
import functools

def redirect_if_logged_in(func):
    functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)
    return wrapper
