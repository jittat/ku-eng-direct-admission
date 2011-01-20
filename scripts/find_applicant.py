#!/usr/bin/env python

import sys
if len(sys.argv) != 2:
    print "Usage: find_applicant [national_id]"
    quit()

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

nat_id = sys.argv[1]

from application.models import Applicant

a = Applicant.objects.get(national_id=nat_id)
print u"%s,%s" % (a.full_name(), a.email)
