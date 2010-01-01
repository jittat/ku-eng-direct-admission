import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import SubmissionInfo, Applicant, Education, PersonalInfo
from utils import get_submitted_applicant_dict

import sys
if len(sys.argv)!=2:
    print "Usage: export_anet [output.csv]"
    quit()
file_name = sys.argv[1]

applicants = get_submitted_applicant_dict(
    { 'personal_info': PersonalInfo,
      'education': Education,
      'submission_info': SubmissionInfo })

f = codecs.open(file_name, encoding="utf-8", mode="w")
for applicant in applicants.itervalues():
    if applicant.submission_info.doc_reviewed_complete and not applicant.education.uses_gat_score:
        print >> f, (u"%s,%s,%s,%d" % 
                     (applicant.personal_info.national_id, 
                      applicant.first_name, applicant.last_name,
                      applicant.education.anet))

