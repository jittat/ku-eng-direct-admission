import codecs

import sys
if len(sys.argv)!=2:
    print "Usage: import_final_results [results.csv]"
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
    for l in lines[1:]:
        items = l.strip().split(',')
        app = {'national_id': items[0],
               'major': items[2] }
        applicants.append(app)

def standardize_major_number(major):
    return ('0' * (3 - len(major))) + major

def import_results():
    print 'Importing results...'

    majors = Major.get_all_majors()
    major_dict = dict([(m.number, m) for m in majors])

    not_found_list = []

    app_order = 1
    for a in applicants:
        personal_infos = (PersonalInfo.objects
                         .filter(national_id=a['national_id'])
                         .select_related(depth=1))

        if len(personal_infos)==0:
            print "NOT-FOUND:", a['national_id']
            not_found_list.append(a['national_id'])
            continue

        for pinfo in personal_infos:
            
            applicant = pinfo.applicant
            try:
                aresult = applicant.admission_result
            except:
                aresult = AdmissionResult.new_for_applicant(applicant)

            major_number = standardize_major_number(a['major'])
            major = major_dict[major_number]
            
            aresult.is_final_admitted = True
            aresult.final_admitted_major = major

            aresult.save()

        print a['national_id']

    print '-------NOT-FOUND-------'
    for nid in not_found_list:
        print nid

def main():
    read_results()
    import_results()

if __name__ == '__main__':
    main()
