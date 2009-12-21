from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, SubmissionInfo
from review.models import ReviewField, ReviewFieldResult
from commons.models import Log

def main():
    REMOVED_FIELDS = ['picture', 
                      'nat_id',
                      'gat_score',
                      'pat1_score',
                      'pat3_score',
                      'anet_score',
                      'abroad_edu_certificat']

    for applicant in Applicant.objects.all():
        if ((not applicant.is_submitted) or 
            (applicant.submission_info.doc_reviewed_complete)):
            continue
        else:
            review_results = ReviewFieldResult.objects.filter(applicant=applicant)
            if len(review_results)==0:
                # have no reviews
                continue

            print applicant.ticket_number(), applicant.full_name(),

            passed = True
            changed = False
            for r in review_results:
                if not r.is_passed:
                    f = ReviewField.get_field_by_id(r.review_field_id)
                    if f.short_name in REMOVED_FIELDS:
                        print f.short_name, '(fixed)',
                        r.is_passed = True
                        r.internal_note = r.internal_note + '(fixed by admin)'
                        r.save()
                        msg = ('Updated ReviewFieldResult (id:%d) %s for %d, set to passed' %
                               (r.id, f.short_name, applicant.id))
                        Log.create(msg, 'console', 
                                   applicant_id=applicant.id,
                                   applicantion_id=applicant.submission_info.applicantion_id)
                        changed = True
                    else:
                        passed = False
            if changed and passed:
                print 'PASSED'
                applicant.submission_info.doc_reviewed_complete = True
                applicant.submission_info.save()
                msg = ('Updated SubmissionInfo (id:%d) for %d, set doc_reviewed_complete to True' % (applicant.submission_info.applicantion_id, applicant.id))
                Log.create(msg, 'console',
                           applicant_id=applicant.id,
                           applicantion_id=applicant.submission_info.applicantion_id)
            else:
                print 'FAILED'

if __name__ == '__main__':
    main()
            
        
            

