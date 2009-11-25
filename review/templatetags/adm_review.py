import os

from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('review/tags/doc_view_link.html')
def doc_view(applicant, field_name):
    appdocs = applicant.get_applicant_docs_or_none()
    if appdocs:
        filename = appdocs.__getattribute__(field_name).name
        name, ext = os.path.splitext(filename)
    else:
        ext = 'png'

    filename = '%s%s' % (field_name, ext)

    return { 'applicant': applicant,
             'field_name': field_name,
             'filename': filename }
