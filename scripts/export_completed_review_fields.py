import sys

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, PersonalInfo
from review.models import ReviewField, ReviewFieldResult
from utils import get_submitted_applicant_dict

applicant_nat_ids = {}
for pinfo in PersonalInfo.objects.all():
    applicant_nat_ids[pinfo.applicant_id] = pinfo.national_id

completed_review_fields = {}
for result in ReviewFieldResult.objects.all():
    if not result.is_passed:
        continue
    app_id = result.applicant_id
    if app_id in applicant_nat_ids:
        nat_id = applicant_nat_ids[app_id]
        if nat_id not in completed_review_fields:
            completed_review_fields[nat_id] = []
        completed_review_fields[nat_id].append(result.review_field_id)
    else:
        print "App not found (%d)" % (app_id,)

review_fields = dict([(r.id, r.short_name) 
                      for r in ReviewField.objects.all()])

for nat_id in completed_review_fields.keys():
    fields = completed_review_fields[nat_id]

    data = [nat_id] + [review_fields[f] for f in fields]
    print ','.join(data)
