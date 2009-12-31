import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import SubmissionInfo, Applicant, PersonalInfo
from utils import get_submitted_applicant_dict

import sys
if len(sys.argv)!=2:
    print "Usage: clean_dup [output.csv]"
    quit()
file_name = sys.argv[1]
f = codecs.open(file_name, encoding="utf-8", mode="w")

def print_applicant(f, applicant):
    if applicant.is_submitted:
        if applicant.submission_info.doc_reviewed_complete:
            print >> f, applicant.ticket_number(), applicant.full_name(), 'PASSED'
        else:
            print >> f, applicant.ticket_number(), applicant.full_name()
    else:
        print >> f, 'ID:', applicant.id, applicant.full_name()

def print_dup(f, applicants):
    for app in applicants:
        print_applicant(f, app)

def find_dup(f, applicants, key_func):
    keys = {}
    for app in applicants:
        k = key_func(app)
        if k not in keys:
            keys[k] = []
        keys[k].append(app)
    for k, applicants in keys.iteritems():
        if len(applicants)>1:
            print_dup(f, applicants)
            print >>f

def get_national_id(applicant):
    return applicant.personal_info.national_id

def get_fullname(applicant):
    first_name = applicant.first_name.strip()
    last_name = applicant.last_name.strip()
    return first_name + ' ' + last_name

def main():
    applicants = get_submitted_applicant_dict(
        { 'personal_info': PersonalInfo,
          'submission_info': SubmissionInfo })

    print >>f, 'National ID'
    print >>f, '-----------'
    find_dup(f, applicants.itervalues(), get_national_id)

    print
    print >>f, "Applicants' name"
    print >>f, '----------------'
    find_dup(f, applicants.itervalues(), get_fullname)


if __name__ == '__main__':
    main()
