from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, SubmissionInfo
from review.models import ReviewField, ReviewFieldResult

def main():
    REMOVED_FIELDS = ['picture', 
                      'nat_id',
                      'gat_score',
                      'pat1_score',
                      'pat3_score',
                      'anet_score',
                      'abroad_edu_certificat']

    for applicant in Applicant.objects.all():
        if not applicant.is_submitted:
            continue
        if applicant.submission_info.doc_reviewed_complete:
            continue
        else:
            print applicant.ticket_number(), applicant.full_name(), 'FAILED:',
            review_results = ReviewFieldResult.objects.filter(applicant=applicant)
            if len(review_results)==0:
                print 'Not reviewed'
                continue

            for r in review_results:
                if not r.is_passed:
                    f = ReviewField.get_field_by_id(r.review_field_id)
                    print f.short_name,
            print 

if __name__ == '__main__':
    main()
            
        
            

