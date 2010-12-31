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


EXAM_COUNT = 6

f = open(file_name)

for line in f:
    items = line.split(',')
    if len(items)>0 and len(items) != 1 + 3*EXAM_COUNT:
        print 'Score file format error'
        quit()

    nat_id = items[0]
    print nat_id
    apps = Applicant.objects.filter(national_id=nat_id)
    if len(apps)!=1:
        print 'Error applicant:', nat_id
        continue

    app = apps[0]
    try:
        scores = app.NIETS_scores
    except:
        scores = NIETSScores()

    scores.score_list = ','.join(items[1:])
    scores.applicant = app
    scores.save()
