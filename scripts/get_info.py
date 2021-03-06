import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import SubmissionInfo, Applicant, PersonalInfo
from utils import get_submitted_applicant_dict

applicants = get_submitted_applicant_dict(
    {'personal_info': PersonalInfo}
    )

nat_id_dict = dict([(app.personal_info.national_id, app) 
                    for app in applicants.itervalues()])

def main():
    while True:
        try:
            line = raw_input()
            if line in nat_id_dict:
                app = nat_id_dict[line]
                print ("%s %s %s %s" % 
                       (line, app.full_name(), 
                        app.email,
                        app.personal_info.phone_number))
            else:
                print line, "not found"
        except:
            break

if __name__ == '__main__':
    main()

