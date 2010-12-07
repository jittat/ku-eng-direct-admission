#!/usr/bin/env python
import sys
if len(sys.argv)!=3:
    print "Usage: python paid.py [nat_id] [verification num]"
    quit()

import os
import datetime

path = os.path.dirname(__file__)
parent_path = os.path.abspath(os.path.join(path, '..'))
sys.path.append(parent_path)

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant

national_id = sys.argv[1]
verification = sys.argv[2]

applicants = Applicant.objects.filter(national_id=national_id)
if len(applicants)!=0:
    applicant = applicants[0]
    try:
        submission_info = applicant.submission_info
    except:
        print "ERROR (no submission info):", applicant
        quit()
                
    if applicant.verification_number() != verification:
        print "ERROR:", applicant, applicant.verification_number(), verification
    else:
        submission_info.is_paid = True
        submission_info.paid_at = datetime.datetime.today()
        submission_info.save()
        print "Updated: ", applicant
else:
    print "ERROR: NAT ID NOT FOUND", national_id
