#!/usr/bin/env python
import sys
if len(sys.argv)!=5:
    print "Usage: python confirm_one.py [round_number] [national_id] [verification] [amount]"
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


def main():
    round_number = int(sys.argv[1])
    national_id = sys.argv[2]
    verification = sys.argv[3]
    amount = int(sys.argv[4])

    try:
        applicant = Applicant.objects.get(national_id=national_id)
    except:
        print "NAT NOT FOUND"
        quit()

    results = applicant.admission_results.filter(round_number=round_number).all()
    if len(results)!=0:
        result = results[0]
    else:
        result = None
    if result == None:
        print "ERROR (no admission result):", applicant, national_id
        quit()

    expected_verification = applicant.verification_number(settings.CONFIRMATION_HASH_MAGIC)
    if expected_verification != verification:
        print "ERROR (verification):", applicant, national_id, expected_verification, verification
        quit()

    confirmations = applicant.admission_confirmations.filter(round_number=round_number)
    if len(confirmations)!=0:
        print "ERROR (dup):", applicant, national_id, confirmations[0].paid_amount, confirmations[0].confirmed_at
        quit()

    confirmation = AdmissionConfirmation()
    confirmation.applicant = applicant
    confirmation.paid_amount = amount
    confirmation.round_number = round_number
    confirmation.save()
    print "DONE"

if __name__=='__main__':
    main()
