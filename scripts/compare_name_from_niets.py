import codecs
import csv

import sys
if len(sys.argv)!=3:
    print "Usage: import_name_from_niets [result_from_niets.csv] [compare_result]"
    quit()
file_name = sys.argv[1]
out_file_name = sys.argv[2]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, PersonalInfo

def check_app_name(app, first_name, last_name):
    return ((app.first_name.strip() == first_name) and 
            (app.last_name.strip() == last_name))

infos = PersonalInfo.objects.select_related(depth=1).all()
info_dict = {}
for i in infos:
    if i.national_id in info_dict:
        info_dict[i.national_id].append(i)
    else:
        info_dict[i.national_id] = [i]

f = codecs.open(file_name, encoding='utf-8')
fout = codecs.open(out_file_name, encoding='utf-8', mode='w')

for line in f:
    items = line.split(',')
    personal_infos = info_dict[items[0]]
    for p in personal_infos:
        if not check_app_name(p.applicant, items[1], items[2]):
            print >> fout, "%s,%s,%s,%s,%s" % (
                p.national_id, p.applicant.first_name, p.applicant.last_name, 
                items[1], items[2])
