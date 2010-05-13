# -*- coding: utf-8 -*-
import os

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import datetime, timedelta

def redirect_to_index(request):
    # clear user session
    if 'applicant_id' in request.session:
        del request.session['applicant_id']
    # go back to front page, will be changed later
    return HttpResponseRedirect(reverse(settings.INDEX_PAGE))

def redirect_to_deadline_error():
    return HttpResponseRedirect(reverse('commons-deadline-error'))

def time_to_submission_deadline():
    try:
        deadline = settings.SUBMISSION_DEADLINE
        if deadline != None:
            return deadline - datetime.now()
        else:
            return timedelta.max
    except:
        pass
    return timedelta.max  # no deadline

def time_to_supplement_submission_deadline():
    try:
        deadline = settings.SUPPLEMENT_DEADLINE
        if deadline != None:
            return deadline - datetime.now()
        else:
            return timedelta.max
    except:
        pass
    return timedelta.max  # no deadline

def time_to_round2_confirmation_deadline():
    try:
        deadline = settings.ROUND2_CONFIRMATION_DEADLINE
        if deadline != None:
            return deadline - datetime.now()
        else:
            return timedelta.max
    except:
        pass
    return timedelta.max  # no deadline


def submission_deadline_passed():
    try:
        deadline = settings.SUBMISSION_DEADLINE
        if deadline != None:
            return datetime.now() >= deadline
        else:
            return False
    except:
        pass
    return False

def supplement_submission_deadline_passed():
    try:
        deadline = settings.SUPPLEMENT_DEADLINE
        if deadline != None:
            return datetime.now() >= deadline
        else:
            return False
    except:
        pass
    return False

def round2_confirmation_deadline_passed():
    try:
        deadline = settings.ROUND2_CONFIRMATION_DEADLINE
        if deadline != None:
            return datetime.now() >= deadline
        else:
            return False
    except:
        pass
    return False

    

def admission_major_pref_deadline_passed():
    try:
        deadline = settings.ADMISSION_MAJOR_PREF_DEADLINE
        if deadline != None:
            return datetime.now() >= deadline
        else:
            return False
    except:
        pass
    return False
        

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

def extract_variable_from_session_or_none(session, name):
    value = None
    if name in session:
        try:
            value = session[name]
            del session[name]
        except KeyError:
            pass
    return value



