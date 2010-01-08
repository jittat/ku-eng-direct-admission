import codecs

import sys
if len(sys.argv)!=2:
    print "Usage: import_results_for_private_display [results.csv]"
    quit()

file_name = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import AdmissionResult
from application.models import Applicant, SubmissionInfo, PersonalInfo, Major

applicants = []

def read_results():
    f = codecs.open(file_name, encoding="utf-8", mode="r")
    lines = f.readlines()
    order = 1
    for l in lines:
        items = l.split(',')
        app = {'order': order,
               'ticket_number': items[0],
               'first_name': items[1],
               'last_name': items[2],
               'national_id': items[3],
               'major': items[4] }
        if len(items)>=6:
            app['additional_info'] = items[5]
        applicants.append(app)
        order += 1

def delete_old_admission_results():
    AdmissionResult.objects.all().delete()

def standardize_major_number(major):
    return ('0' * (3 - len(major))) + major

def import_results():
    print 'Importing results...'

    delete_old_admission_results()

    majors = Major.get_all_majors()
    major_dict = dict([(m.number, m) for m in majors])

    app_order = 1
    for a in applicants:
        personal_infos = (PersonalInfo.objects
                         .filter(national_id=a['national_id'])
                         .select_related(depth=1))

        for pinfo in personal_infos:
            
            aresult = AdmissionResult()
            aresult.applicant = pinfo.applicant
            if a['major']=='wait':
                aresult.is_admitted = False
                aresult.is_waitlist = True
                aresult.admitted_major = None
                aresult.additional_info = a['additional_info']
            else:
                major_number = standardize_major_number(a['major'])
                major = major_dict[major_number]
            
                aresult.is_admitted = True
                aresult.is_waitlist = False
                aresult.admitted_major = major
                aresult.additional_info = a['additional_info']

            aresult.save()

        print a['ticket_number']

def main():
    read_results()
    import_results()

if __name__ == '__main__':
    main()
