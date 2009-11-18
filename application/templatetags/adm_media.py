from django.template import Library
from django.conf import settings

register = Library()

def media_url():
    """
    Returns the string contained in the setting MEDIA_URL.
    """
    return settings.MEDIA_URL
media_url = register.simple_tag(media_url)


def passed_icon(is_passed=True):
    if is_passed:
        img_src="/image/Clear.png"
    else:
        img_src="/image/MinusRed.png"
    return "%s%s" % (settings.MEDIA_URL, img_src)
passed_icon = register.simple_tag(passed_icon)

