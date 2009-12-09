import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

import sys

if len(sys.argv)!=2:
    print "Usage: export_applicants [output.csv]"
    quit()
file_name = sys.argv[1]

from application.models import SubmissionInfo, Applicant, PersonalInfo

apps = {}
for app in Applicant.objects.all():
    apps[app.id] = [app.first_name, app.last_name,'']

for personal_info in PersonalInfo.objects.all():
    app_id = personal_info.applicant_id
    if app_id in apps:
        apps[app_id].append(personal_info.national_id)
    else:
        print 'problem with', app_id

f = codecs.open(file_name, encoding="utf-8", mode="w")
print >> f, "No,CITIZENID,Name,SurName"
i = 0
for submission_info in SubmissionInfo.objects.all():
    app_id = submission_info.applicant_id
    print >> f, "%d,%s,%s,%s" % ((i+1), apps[app_id][3], apps[app_id][0], apps[app_id][1])
    i += 1
