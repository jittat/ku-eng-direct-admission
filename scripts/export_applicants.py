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


applicants = get_submitted_applicant_dict(
    {'personal_info': PersonalInfo,
     'submission_info': SubmissionInfo })

f = codecs.open(file_name, encoding="utf-8", mode="w")
print >> f, "No,CITIZENID,Name,SurName"
i = 0

appeared = {}

for applicant in applicants.itervalues():
    if not applicant.submission_info.is_paid:
        continue
    nat_id = applicant.national_id
    if nat_id not in appeared:
        print >> f, '%d,"%s","%s","%s"' % (
            (i+1), 
            applicant.personal_info.national_id, 
            applicant.first_name,
            applicant.last_name)
        i += 1
        appeared[nat_id] = True


