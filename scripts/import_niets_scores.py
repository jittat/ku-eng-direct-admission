import codecs

import sys
if len(sys.argv)!=2:
    print "Usage: import_niets_scores [combined_scores.csv]"
    quit()

file_name = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import NIETSScores
from application.models import Applicant, PersonalInfo

infos = PersonalInfo.objects.select_related(depth=1).all()
info_dict = {}
for i in infos:
    if i.national_id in info_dict:
        info_dict[i.national_id].append(i)
    else:
        info_dict[i.national_id] = [i]

f = open(file_name)

for line in f:
    items = line.split(',')
    if len(items)>0 and len(items)!=12:
        print 'Score file format error'
        quit()

    print items[0]
    personal_infos = info_dict[items[0]]
    for p in personal_infos:
        app = p.applicant
        try:
            scores = app.NIETS_scores
        except:
            scores = NIETSScores()

        scores.score_list = ','.join(items[3:])
        scores.applicant = app
        scores.save()
