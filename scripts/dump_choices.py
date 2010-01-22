import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant
from confirmation.models import AdmissionMajorPreference, AdmissionConfirmation

def main():
    prefs = AdmissionMajorPreference.objects.all()
    counts = dict([(i,0) for i in [1,2,3,4]])

    for p in prefs:
        pref_type = p.get_pref_type()
        counts[pref_type.ptype] += 1

    print 'all:'
    print counts
    
    con_counts = dict([(i,0) for i in [1,2,3,4]])
    confirmed = AdmissionConfirmation.objects.all()
    for c in confirmed:
        p = None
        try:
            if c.applicant.admission_major_preference != None:
                p = c.applicant.admission_major_preference
        except:
            pass
        if p!=None:
            pref_type = p.get_pref_type()
            con_counts[pref_type.ptype] += 1
    
    print 'confirmed:'
    print con_counts

if __name__ == '__main__':
    main()
    
