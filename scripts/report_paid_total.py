import codecs

import sys
if len(sys.argv)!=2:
    print "Usage: report_paid_total.py [result_file]"
    quit()

filename = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant

lines = open(filename).readlines()

for l in lines:
    nat_id,maj = l.strip().split(',')
    a = Applicant.objects.get(national_id=nat_id)
    p = 0
    for c in a.admission_confirmations.all():
        p += c.paid_amount

    maj = int(maj)

    if maj < 100:
        r = 16000
    elif maj < 200:
        r = 36700
    else:
        r = 60700

    print "%s,%s,%d,%d,%d" % (a.national_id, a.full_name(), maj, r, p)

