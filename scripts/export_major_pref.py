import codecs

import sys
if len(sys.argv)!=2:
    print "Usage: export_major_pref [output.csv]"
    quit()
file_name = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import SubmissionInfo, Applicant, Major, MajorPreference, PersonalInfo
from utils import get_submitted_applicant_dict

applicants = get_submitted_applicant_dict({
        'preference': MajorPreference,
        'personal_info': PersonalInfo,
        })

f = codecs.open(file_name, encoding="utf-8", mode="w")
for applicant in applicants.itervalues():
    majors_str = ",".join([str(m) for m in  applicant.preference.majors])
    print >> f, "%s,%s,%d,%s" % (
        applicant.ticket_number(),
        applicant.personal_info.national_id,
        len(applicant.preference.majors),
        majors_str)
