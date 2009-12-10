import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import SubmissionInfo, Applicant, PersonalInfo
from utils import get_submitted_applicant_dict

import sys
if len(sys.argv)!=2:
    print "Usage: export_applicants [output.csv]"
    quit()
file_name = sys.argv[1]


applicants = get_submitted_applicant_dict({'personal_info': PersonalInfo})

f = codecs.open(file_name, encoding="utf-8", mode="w")
for applicant in applicants.itervalues():
    print >> f, "%s,%s,%s,%s" % (
        applicant.ticket_number(),
        applicant.personal_info.national_id, 
        applicant.first_name,
        applicant.last_name)
