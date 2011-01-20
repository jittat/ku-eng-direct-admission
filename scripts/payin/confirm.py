#!/usr/bin/env python
import sys
if len(sys.argv)!=3:
    print "Usage: python confirm.py [round_number] [payin.txt]"
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
from confirmation.models import AdmissionConfirmation
from result.models import AdmissionResult

round_number = int(sys.argv[1])
filename = sys.argv[2]

lines = open(filename).readlines()

updated_count = 0
error_count = 0

for ln in lines:
    if len(ln)!=0 and ln[0]=='D':
        items = ln[84:].strip().split()
        national_id = items[0]
        verification = items[1]
        amount = int(items[2][-10:-5])

        applicants = Applicant.objects.filter(national_id=national_id)
        if len(applicants)!=0:
            applicant = applicants[0]

            result = applicant.get_latest_admission_result()
            if result == None:
                print "ERROR (no admission result):", applicant, national_id
                error_count += 1
                continue

            if applicant.verification_number(settings.CONFIRMATION_HASH_MAGIC) != verification:
                print "ERROR (verification):", applicant, national_id, applicant.verification_number(), verification
                error_count += 1
                continue

            confirmations = applicant.admission_confirmations.filter(round_number=round_number)
            if len(confirmations)!=0:
                print "ERROR (dup):", applicant, national_id, confirmations[0].paid_amount, confirmations[0].confirmed_at
                error_count += 1
                continue

            confirmation = AdmissionConfirmation()
            confirmation.applicant = applicant
            confirmation.amount = amount
            confirmation.round_number = round_number
            confirmation.save()
            updated_count += 1
        else:
            print "ERROR: NAT ID NOT FOUND", national_id

print updated_count, 'updated, with ', error_count, 'errors'
