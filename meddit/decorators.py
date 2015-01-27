from django.shortcuts import render, get_object_or_404
from .models import Post, UrlEntry
from django.core.exceptions import PermissionDenied

def user_owns_url_or_admin(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            url = get_object_or_404(UrlEntry, extension=kwargs['ext'])
            if not request.user.is_superuser and url.author != request.user:
                raise PermissionDenied()
            return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator(function)

