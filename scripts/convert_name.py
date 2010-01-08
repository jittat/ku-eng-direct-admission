import codecs
import csv

import sys
if len(sys.argv)!=2:
    print "Usage: convert_name.py [convert_data]"
    quit()
file_name = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, PersonalInfo

infos = PersonalInfo.objects.select_related(depth=1).all()
info_dict = {}
for i in infos:
    if i.national_id in info_dict:
        info_dict[i.national_id].append(i)
    else:
        info_dict[i.national_id] = [i]

f = codecs.open(file_name, encoding='utf-8')

for line in f:
    items = line.split(',')
    personal_infos = info_dict[items[0]]
    for p in personal_infos:
        p.applicant.first_name = items[3]
        p.applicant.last_name = items[4]
        p.applicant.save()
