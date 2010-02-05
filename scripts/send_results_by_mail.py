from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

import time

from application.models import Applicant, PersonalInfo
from commons.email import send_final_admission_status_by_mail

def main():
    print 'Sending mails...'

    while True:
        try:
            nat_id = raw_input().strip()
        except:
            break

        personal_infos = (PersonalInfo.objects
                         .filter(national_id=nat_id)
                         .select_related(depth=1))

        emails = {}
        for pinfo in personal_infos:
            if pinfo.applicant.email not in emails:
                emails[pinfo.applicant.email] = pinfo.applicant

        for email, app in emails.iteritems():
            print email, app.full_name()
            send_final_admission_status_by_mail(app)
            time.sleep(5)

if __name__ == '__main__':
    main()
