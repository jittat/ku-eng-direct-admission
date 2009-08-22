from django.template import Library

register = Library()

def media_url():
    """
    Returns the string contained in the setting MEDIA_URL.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_URL
media_url = register.simple_tag(media_url)
