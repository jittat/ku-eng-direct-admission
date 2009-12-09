import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import SubmissionInfo, Applicant, Major, MajorPreference
from utils import get_submitted_applicant_dict

import sys
if len(sys.argv)!=2:
    print "Usage: export_major_pref [output.csv]"
    quit()
file_name = sys.argv[1]

applicants = get_submitted_applicant_dict({'preference': MajorPreference})

f = codecs.open(file_name, encoding="utf-8", mode="w")
i = 0
for applicant in applicants.itervalues():
    print >> f, "%d,%s,%s" % (
        (i+1), 
        applicant.ticket_number(),
        applicant.preference.majors)
    i += 1
