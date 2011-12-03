import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant

filename = '../data/central_adm/scores.txt'

for l in open(filename).readlines():
    id = l.strip()
    a = Applicant.objects.filter(national_id=id)
    if a.count()==0:
        print "Not found: ", id
    else:
        try:
            app = a[0]
            score = app.NIETS_scores.get_score()
            print app.national_id, score
        except:
            print "Error: ", id
