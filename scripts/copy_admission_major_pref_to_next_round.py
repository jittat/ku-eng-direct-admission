import codecs

import sys
if len(sys.argv) < 2:
    print "Usage: copy_admission_major_pref_to_next_round [current_round_number]"
    quit()

round_number = int(sys.argv[1])

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant
from confirmation.models import AdmissionMajorPreference
from result.models import AdmissionResult

def main():
    next_round = round_number + 1
    results = AdmissionResult.objects.filter(round_number=next_round).select_related(depth=1)

    for r in results:
        a = r.applicant
        amp = a.get_admission_major_preference(next_round)

        if amp:
            # already exists
            continue

        all_major_prefs = list(a.admission_major_preferences.all())
        if len(all_major_prefs)>0:
            latest_admission_major_pref = all_major_prefs[0]
            admission_major_pref = (
                AdmissionMajorPreference.new_for_applicant(
                    a,
                    latest_admission_major_pref.is_accepted_list))
            admission_major_pref.round_number = next_round
            admission_major_pref.set_ptype_cache()
            print a.national_id, 'copied'

if __name__ == '__main__':
    main()
