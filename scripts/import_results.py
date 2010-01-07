import codecs

import sys
if len(sys.argv)!=3:
    print "Usage: import_results [result_set_id] [results.csv]"
    quit()

result_set_id = int(sys.argv[1])
if result_set_id==0:
    print "Result set id error"
    quit()

file_name = sys.argv[2]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import ReportCategory, QualifiedApplicant
from application.models import Applicant, SubmissionInfo

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
               'last_name': items[2] }
        applicants.append(app)
        order += 1

def delete_results_in_result_set():
    for cat in ReportCategory.objects.filter(result_set_id=result_set_id).all():
        cat.qualifiedapplicant_set.all().delete()
            
def import_report_category():
    print 'Importing categories...'
    ReportCategory.objects.filter(result_set_id=result_set_id).all().delete()

    cat_order = 1
    categories = set()
    for a in applicants:
        name = ReportCategory.get_category_name_from_first_name(a['first_name'])
        if name not in categories:
            categories.add(name)
            rep_cat = ReportCategory(name=name, 
                                     order=cat_order,
                                     result_set_id=result_set_id)
            rep_cat.save()
            cat_order += 1
            print name,
    print 'added.'

def import_results():
    print 'Importing results...'

    app_order = 1
    for a in applicants:
        q_app = QualifiedApplicant()
        q_app.order = app_order
        q_app.ticket_number = a['ticket_number']
        q_app.first_name = a['first_name']
        q_app.last_name = a['last_name']
        q_app.category = ReportCategory.get_category_by_app_first_name(
            result_set_id, a['first_name'])
        submission_info = SubmissionInfo.find_by_ticket_number(a['ticket_number'])
        if submission_info == None:
            print 'TICKET:', a['ticket_number']
        applicant = submission_info.applicant
        q_app.applicant = applicant
        q_app.save()
        app_order += 1

        print a['ticket_number']

def main():
    read_results()
    delete_results_in_result_set()
    import_report_category()
    import_results()

if __name__ == '__main__':
    main()
