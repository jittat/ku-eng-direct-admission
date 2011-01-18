import codecs

import sys
if len(sys.argv) < 3:
    print "Usage: import_results_for_private_display [round_number] [results.csv] [--force]"
    quit()

round_number = int(sys.argv[1])
file_name = sys.argv[2]
if len(sys.argv)>3:
    is_force = sys.argv[3]=="--force"
else:
    is_force = False

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import AdmissionResult
from application.models import Applicant, SubmissionInfo, PersonalInfo, Major

def read_results():
    f = codecs.open(file_name, encoding="utf-8", mode="r")
    lines = f.readlines()[1:]
    order = 1
    applicant_data = []
    for l in lines:
        items = l.strip().split(',')
        app = {'order': order,
               'national_id': items[0],
               'major': items[2] }
        applicant_data.append(app)
        order += 1
    return applicant_data

def delete_old_admission_results(round_number):
    AdmissionResult.objects.filter(round_number=round_number).delete()

def standardize_major_number(major):
    return ('0' * (3 - len(major))) + major

def import_results(round_number, applicant_data):
    print 'Importing results...'

    delete_old_admission_results(round_number)

    majors = Major.get_all_majors()
    major_dict = dict([(m.number, m) for m in majors])

    app_order = 1
    for a in applicant_data:
        applicant = Applicant.objects.get(national_id=a['national_id'])
        aresult = AdmissionResult()
        aresult.applicant = applicant
        aresult.round_number = round_number
        if a['major']=='wait':
            aresult.is_admitted = False
            aresult.is_waitlist = True
            aresult.admitted_major = None
        else:
            major_number = standardize_major_number(a['major'])
            major = major_dict[major_number]
            
            aresult.is_admitted = True
            aresult.is_waitlist = False
            aresult.admitted_major = major

        aresult.save()

        print a['national_id']

def main():
    # make sure not to screw up previous round results
    if AdmissionResult.objects.filter(round_number=round_number).count()!=0:
        if not is_force:
            print "Old results exist.  If you want to overwrite, use --force"
            quit()

    applicant_data = read_results()
    import_results(round_number, applicant_data)

if __name__ == '__main__':
    main()
