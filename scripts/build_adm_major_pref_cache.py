from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from confirmation.models import AdmissionMajorPreference

for p in AdmissionMajorPreference.objects.all():
    p.set_ptype_cache()


