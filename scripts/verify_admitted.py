from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, SubmissionInfo, Education, PersonalInfo, MajorPreference, Major
from result.models import NIETSScores, AdmissionResult
from confirmation.models import AdmissionMajorPreference

def read_interview_data(applicants, nat_dict):
    print 'Read interview data...'
    for a in applicants.itervalues():
        a.is_interviewed = False
    for l in open('../data/interviewed_nat_id.txt').readlines():
        l = l.strip()
        if l == '':
            continue
        assigned = False
        for id in nat_dict[l]:
            if id in applicants:
                applicants[id].is_interviewed = True
                assigned = True
        if not assigned:
            print 'Problem with', l

def load_nat_id_index():
    print 'Load national id...'
    nat_id_to_app_id = {}
    for p in PersonalInfo.objects.all():
        if p.national_id in nat_id_to_app_id:
            nat_id_to_app_id[p.national_id].append(p.applicant_id)
        else:
            nat_id_to_app_id[p.national_id] = [p.applicant_id]
    return nat_id_to_app_id
        
def load_applicants_with_scores():
    print 'Load submission_info/applicants...'
    alist = []
    for sinfo in SubmissionInfo.objects.select_related(depth=1).all():
        a = sinfo.applicant
        a.submission_info = sinfo
        alist.append(a)
    applicants = dict([(a.id, a) 
                       for a in alist
                       if a.submission_info.doc_reviewed_complete])
    print len(applicants.keys()),'applicants'

    print 'Load educations...'
    educations = Education.objects.all()
    for edu in educations:
        try:
            applicants[edu.applicant_id].education = edu
        except KeyError:
            pass

    print 'Load test scores...'
    nscores = NIETSScores.objects.all()
    c = 0
    for s in nscores:
        try:
            applicant = applicants[s.applicant_id]
        except KeyError:
            applicant = None

        if applicant:
            applicant.NIETS_scores = s
            #print applicant.id
            c += 1
            applicant.score = s.get_score(applicant.education.gpax)

    print c, 'with scores'

    print 'Load admission results...'
    
    for ar in AdmissionResult.objects.all():
        try:
            applicants[ar.applicant_id].admission_result = ar
        except KeyError:
            nat_id = ar.applicant.personal_info.national_id
            if PersonalInfo.objects.filter(national_id=nat_id).count()<=1:
                print 'Error', nat_id

    return applicants

def filter_out_withdrawn_first_admitted_applicants(applicants):
    aout = {}
    for a in applicants.itervalues():
        try:
            ar = a.admission_result
        except:
            ar = None
        if ar!=None and ar.is_admitted:
            if a.is_interviewed and a.has_confirmed():
                aout[a.id] = a
        else:
            aout[a.id] = a
    return aout
        

def main():
    applicants = load_applicants_with_scores()
    nat_dict = load_nat_id_index()
    read_interview_data(applicants, nat_dict)

    applicants = filter_out_withdrawn_first_admitted_applicants(applicants)

    print len(applicants.keys()), 'left after 1st round'

    print 'Loading preferences...'

    preferences = dict([(p.applicant_id, p.get_major_list()) 
                        for p in MajorPreference.objects.all()])

    for mp in AdmissionMajorPreference.objects.all():
        preferences[mp.applicant_id] = mp.get_accepted_majors()
        #print preferences[mp.applicant_id]

    print 'Find highest missed...'

    highest_missed = {}
    highest_missed_app = {}
    for m in Major.get_all_majors():
        highest_missed[m.id] = 0

    for a in applicants.itervalues():
        try:
            score = a.score
        except:
            score = 0
        try:
            ar = a.admission_result
        except:
            ar = None
        for m in preferences[a.id]:
            if (ar!=None and 
                ar.is_final_admitted and 
                m.id == ar.final_admitted_major_id):
                break
            if score > highest_missed[m.id]:
                highest_missed[m.id] = score
                highest_missed_app[m.id] = a
    for m in Major.get_all_majors():
        print m.number, m.name, highest_missed[m.id], highest_missed_app[m.id].full_name()


if __name__=='__main__':
    main()
