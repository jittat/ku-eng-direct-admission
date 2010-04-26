from django.http import HttpResponseForbidden
from models import Feature

def feature_enabled_required(name):
    def fdecorate(view_function):
        def decorate(request, *args, **kwargs):
            if not Feature.check_enabled(name):
                return HttpResponseForbidden()
            return view_function(request, *args, **kwargs)
        return decorate
    return fdecorate

