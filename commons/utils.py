# -*- coding: utf-8 -*-
import os

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings

def redirect_to_index(request):
    # clear user session
    if 'applicant_id' in request.session:
        del request.session['applicant_id']
    # go back to front page, will be changed later
    return HttpResponseRedirect(reverse(settings.INDEX_PAGE))


def admin_email():
    admin = settings.ADMINS[0]
    return admin[1]

PASSWORD_CHARS = 'abcdefghjkmnopqrstuvwxyz'

def random_string(length=10):
    from random import choice
    s = [choice(PASSWORD_CHARS) for i in range(length)]
    return ''.join(s)       


def serve_file(filename):
    import mimetypes
    import stat
    from django.utils.http import http_date

    statobj = os.stat(filename)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    contents = open(filename, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    response["Content-Length"] = len(contents)
    return response


