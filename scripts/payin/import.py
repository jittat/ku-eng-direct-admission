import sys
import os
import datetime

path = os.path.dirname(__file__)
parent_path = os.path.abspath(os.path.join(path, '..'))
sys.path.append(parent_path)

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant

filename = '../../data/payin/KU3.TXT'

lines = open(filename).readlines()

for ln in lines:
    if len(ln)!=0 and ln[0]=='D':
        items = ln[84:].split()
        national_id = items[0]
        verification = items[1]

        applicants = Applicant.objects.filter(national_id=national_id)
        if len(applicants)!=0:
            applicant = applicants[0]
            submission_info = applicant.submission_info
            if applicant.verification_number() != verification:
                print "ERROR:", applicant, applicant.verification_number(), verification
            else:
                submission_info.is_paid = True
                submission_info.paid_at = datetime.datetime.today()
                submission_info.save()
                print "UPDATED:", applicant
