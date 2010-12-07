#!/usr/bin/env python
import sys
if len(sys.argv)!=2:
    print "Usage: python import.py [payin.txt]"
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

filename = sys.argv[1]

lines = open(filename).readlines()

updated_count = 0
error_count = 0

for ln in lines:
    if len(ln)!=0 and ln[0]=='D':
        items = ln[84:].split()
        national_id = items[0]
        verification = items[1]

        applicants = Applicant.objects.filter(national_id=national_id)
        if len(applicants)!=0:
            applicant = applicants[0]
            try:
                submission_info = applicant.submission_info
            except:
                error_count += 1
                print "ERROR (no submission info):", applicant, applicant.verification_number(), verification
                continue
                
            if applicant.verification_number() != verification:
                print "ERROR:", applicant, national_id, applicant.verification_number(), verification
                error_count += 1
            else:
                submission_info.is_paid = True
                submission_info.paid_at = datetime.datetime.today()
                submission_info.save()
                updated_count += 1
        else:
            print "ERROR: NAT ID NOT FOUND", national_id

print updated_count, 'updated, with ', error_count, 'errors'
