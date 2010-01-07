import codecs

import sys
if len(sys.argv)!=4:
    print "Usage: report_result_as_csv [assignment.csv] [pref.csv] [result.csv]"
    quit()
assignment_file_name = sys.argv[1]
pref_file_name = sys.argv[2]
out_file_name = sys.argv[3]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, SubmissionInfo

def read_as_dict(file_name, key_field, header_row=False):
    f = codecs.open(file_name, encoding='utf-8')
    d = {}
    if header_row:
        f.readline()
    for line in f:
        items = line.strip().split(',')
        d[items[key_field]] = items
    return d

pref_dict = read_as_dict(pref_file_name,1)
assignment_dict = read_as_dict(assignment_file_name, 0, header_row=True)

f = codecs.open(out_file_name, encoding='utf-8', mode='w')

for nat_id, data in assignment_dict.iteritems():
    pref = pref_dict[nat_id]
    submission_info = SubmissionInfo.find_by_ticket_number(pref[0])
    applicant = submission_info.applicant
    print >> f, pref[0] + ',' + applicant.first_name + ',' + applicant.last_name + ',' + ','.join(data) + ',"' + ','.join(pref[3:]) + '"'

