import codecs
import csv

import sys
if len(sys.argv)!=2:
    print "Usage: convert_nat_id [nat_id_conversion.csv]"
    quit()
file_name = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import PersonalInfo

reader = csv.reader(open(file_name))
reader.next()  # throw away first line

nat_id_map = dict([(item[0],item[1]) for item in reader])

for old_id, new_id in nat_id_map.iteritems():
    print "%s -> %s" % (old_id, new_id)

    infos = list(PersonalInfo.objects.filter(national_id=old_id))

    if len(infos)!=0:
        for p in infos:
            p.national_id = new_id
            p.save()
    else:
        print 'Not found'

