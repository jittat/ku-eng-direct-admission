import sys

if len(sys.argv)!=2:
    print "Usage: import_completed_review_fields [input.csv]"
    quit()
file_name = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from review.models import ReviewField, CompletedReviewField
from utils import get_submitted_applicant_dict

review_fields = dict([(r.short_name, r)
                      for r in ReviewField.objects.all()])

for line in open(file_name):
    items = line.split(',')
    nat_id = items[0]
    fields = items[1:]

    for f in fields:
        if f in review_fields:
            rf = CompletedReviewField(national_id=nat_id,
                                      review_field=review_fields[f])
            rf.save()
    print nat_id
