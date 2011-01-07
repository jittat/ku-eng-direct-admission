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
        'submission_info': SubmissionInfo,
        })

f = codecs.open(file_name, encoding="utf-8", mode="w")

pref = {}

SUBMISSION_RANK = {1: 2, # doc by mail
                   2: 1, # online
                   3: 3} # all by mail

for applicantion_id in sorted(applicants.keys()):
    applicant = applicants[applicantion_id]
    #if not applicant.submission_info.doc_reviewed_complete:
    #    continue
    majors_str = ",".join([str(m) for m in  applicant.preference.majors])
    nat_id = applicant.personal_info.national_id
    submission_method = applicant.doc_submission_method
    output_str = "%s,%s,%d,%s" % (
        applicant.ticket_number(),
        applicant.personal_info.national_id,
        len(applicant.preference.majors),
        majors_str)

    if nat_id in pref:
        old_pref = pref[nat_id]

        if SUBMISSION_RANK[submission_method] > SUBMISSION_RANK[old_pref[1]]:
            print "Old - better: [%s/%d] > [%s/%d]" % (
                old_pref[0], old_pref[1],
                output_str, submission_method)
            continue
        else:
            print "New - better: [%s/%d] > [%s/%d]" % (
                output_str, submission_method,
                old_pref[0], old_pref[1])

    pref[nat_id] = (output_str,
                    submission_method)

for output, method in pref.itervalues():
    print >> f, output
