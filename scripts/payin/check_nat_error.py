import sys
if len(sys.argv)!=2:
    print "Usage: python check_nat_error.py [payin.txt]"
    quit()

import os
import datetime
import codecs

path = os.path.dirname(__file__)
parent_path = os.path.abspath(os.path.join(path, '..'))
sys.path.append(parent_path)

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant

filename = sys.argv[1]

lines = codecs.open(filename, mode='r', encoding='tis-620').readlines()

updated_count = 0
error_count = 0

for ln in lines:
    if len(ln)!=0 and ln[0]=='D':
        name = ln[34:84].strip()
        items = ln[84:].split()
        national_id = items[0]
        verification = items[1]

        applicants = Applicant.objects.filter(national_id=national_id)
        if len(applicants)==0:
            print "ERROR: NAT ID NOT FOUND", name, national_id, verification

print updated_count, 'updated, with ', error_count, 'errors'
