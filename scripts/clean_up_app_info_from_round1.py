from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, PersonalInfo

for a in Applicant.objects.all():
    print a.id
    a.doc_submission_method = Applicant.UNDECIDED_METHOD
    a.is_submitted = False
    a.refresh_has_related_model()
    a.save()
