import sys

if len(sys.argv)!=2:
    print "Usage: export_major_choice.py [round_number]"
    quit()

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from confirmation.models import AdmissionMajorPreference
from application.models import Applicant

def main():
    round_number = int(sys.argv[1])
    mprefs = (AdmissionMajorPreference.
              objects.
              filter(round_number=round_number).
              select_related(depth=1).all())
    for mpref in mprefs:
        alist = mpref.is_accepted_list
        print "%s,%d,%d,%s" % (mpref.applicant.personal_info.national_id,
                               mpref.get_pref_type().ptype,
                               len(alist),
                               ','.join([str(a) for a in alist]))

if __name__ == '__main__':
    main()

