#!/usr/bin/env python
import sys

if len(sys.argv)!=3:
    print "Usage: waive.py [national_id] [Yes/No]"
    quit()

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from confirmation.models import AdmissionWaiver 
from application.models import Applicant

def main():
    national_id = sys.argv[1]
    action = sys.argv[2]
    if action not in ['Yes','No']:
        print 'You must specify Yes or No.'
        quit()

    a = Applicant.objects.get(national_id=national_id)

    print a
    sure = raw_input('Are you sure (Yes/No)? ')
    if sure!='Yes':
        print 'Cancelled'
        quit()

    try:
        w = a.admission_waiver
    except:
        w = AdmissionWaiver(applicant=a)
    
    if action=='Yes':
        w.is_waiver = True
    else:
        w.is_waiver = False

    w.save()
    print 'DONE'


if __name__ == '__main__':
    main()

