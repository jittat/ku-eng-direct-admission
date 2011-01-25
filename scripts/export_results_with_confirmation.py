import sys

if len(sys.argv)!=2:
    print "Usage: export_results_with_confirmation.py [round_number]"
    quit()

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import AdmissionResult
from confirmation.models import AdmissionConfirmation
from application.models import Applicant

def main():
    round_number = int(sys.argv[1])

    results = (AdmissionResult.
               objects.
               filter(round_number=round_number).
               select_related(depth=1).
               all())

    for r in results:
        app = r.applicant
        paid_total = sum([c.paid_amount for c in app.admission_confirmations.all()])
        confirmed = paid_total >= r.admitted_major.confirmation_amount
        print "%s,%d,%s" % (app.national_id, int(r.admitted_major.number), str(confirmed))



if __name__ == '__main__':
    main()

