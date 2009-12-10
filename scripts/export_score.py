import codecs
import sys

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import SubmissionInfo, Applicant, Major, MajorPreference, Education, GPExamDate, PersonalInfo
from utils import get_submitted_applicant_dict

def build_gatpat_id(l):
    gid = {}
    i = 0
    for g in l:
        gid[g] = i
        i += 1
    return gid
gatpat_rounds = sorted([d.id for d in GPExamDate.objects.all()])
gatpat_number = build_gatpat_id(gatpat_rounds)

def extract_gatpat_scores(education):
    """
    extracts GAT/PAT scores as a list with 9 numbers, i.e.,
    [gat-mar,pat1-mar,pat2-mar,gat-jul,pat1-jul,....]
    """
    scores = [0] * 3 * len(gatpat_rounds)
    if education.gat_date_id!=None:
        scores[3 * gatpat_number[education.gat_date_id]] = education.gat
    if education.pat1_date_id!=None:
        scores[1 + 3 * gatpat_number[education.pat1_date_id]] = education.pat1
    if education.pat3_date_id!=None:
        scores[2 + 3 * gatpat_number[education.pat3_date_id]] = education.pat3
    return scores
    

def print_applicant(applicant):
    if applicant.education.uses_gat_score:
        print "%s,%f,gatpat,%s" % (
            applicant.personal_info.national_id,
            applicant.education.gpax,
            ','.join([str(s) for s 
                      in extract_gatpat_scores(applicant.education)]))
    else:
        print "%s,%f,anet,%d" % (
            applicant.personal_info.national_id,
            applicant.education.gpax,
            applicant.education.anet)

applicants = get_submitted_applicant_dict({
        'preference': MajorPreference,
        'personal_info': PersonalInfo,
        'education': Education })

for applicant in applicants.itervalues():
    print_applicant(applicant)

