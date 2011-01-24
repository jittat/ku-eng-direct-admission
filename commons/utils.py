# -*- coding: utf-8 -*-
import os
import re

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

##########################################
#   DEADLINE
#

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
    from result.models import AdmissionRound

    time_to_deadline = AdmissionRound.time_to_recent_round_deadline()

    return time_to_deadline <= timedelta(0)
        

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


def validate_national_id(nat_id):
    if len(nat_id)!=13:
        return False
    s = 0
    for i in range(12):
        try:
            s += int(nat_id[i])*(13-i)
        except:
            return False
    last_num = (11 - (s % 11)) % 10
    return nat_id[12] == str(last_num)


def validate_phone_number(phone_number):
    u"""
    >>> validate_phone_number('081-111-1111')
    True
    >>> validate_phone_number('0811111111')
    True
    >>> validate_phone_number('081-11-1111')
    False
    >>> validate_phone_number('02-942-8555')
    True
    >>> validate_phone_number('029428555')
    True
    >>> validate_phone_number(u'02-942-8555 ต่อ 1234')
    True
    >>> validate_phone_number(u'029428555 ต่อ 1234')
    True
    >>> validate_phone_number('029428555 ext 1234')
    True
    >>> validate_phone_number('029428555 # 1234')
    True
    >>> validate_phone_number('02-942-85554 ต่อ 1234')
    False
    >>> validate_phone_number('034123234')
    True
    """
    if re.match(u'^([0-9\\- #]|ต่อ|ext)+$', phone_number)==None:
        return False
    
    indicies = [index for index in 
                [phone_number.find(ext) for ext in [u'#',u'ต่อ',u'ext']]
                if index != -1]

    if len(indicies)!=0:
        i = min(indicies)
    else:
        i = len(phone_number)

    if i!=-1:
        digits = ''.join([s for s in  phone_number[:i] if s.isdigit()])
        if (len(digits) < 9) or (not digits[0]=='0'):
            return False
        if digits[1]=='8':
            return len(digits)==10
        else:
            return len(digits)==9


if __name__ == "__main__":
    import doctest
    doctest.testmod()
