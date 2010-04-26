from django.template.defaultfilters import stringfilter
from django import template

from feature_switch.models import Feature

register = template.Library()

@register.filter
@stringfilter
def feature_is_enabled(name):
    return Feature.check_enabled(name)
