import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant
from confirmation.models import AdmissionMajorPreference

def main():
    prefs = AdmissionMajorPreference.objects.all()
    counts = dict([(i,0) for i in [1,2,3,4]])

    for p in prefs:
        pref_type = p.get_pref_type()
        counts[pref_type.ptype] += 1

    print counts

if __name__ == '__main__':
    main()
    
