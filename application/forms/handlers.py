# -*- coding: utf-8 -*-

from django.conf import settings

from application.models import Major, MajorPreference
from application.forms import EducationForm

def extract_ranks(post_data, major_list):
    """
    extracts a list of majors from post data.  Each select list has an
    id of the form 'major_ID'.
    """
    
    rank_dict = {}
    for m in major_list:
        sel_id = m.select_id()
        if sel_id in post_data:
            r = post_data[sel_id]
            try:
                rnum = int(r)
            except:
                rnum = -1
            if (rnum >= 1) and (rnum <= settings.MAX_MAJOR_RANK):
                rank_dict[rnum] = int(m.number)

    ranks = []
    for r in sorted(rank_dict.keys()):
        ranks.append(rank_dict[r])
    return ranks


def handle_major_form(request):
    applicant = request.applicant
    majors = Major.get_all_majors()

    errors = None

    #print extract_ranks(request.POST, majors)

    major_ranks = extract_ranks(request.POST, majors)
    if len(major_ranks)==0:
        # chooses no majors
        errors = ['ต้องเลือกอย่างน้อยหนึ่งอันดับ']
    else:
        if applicant.has_major_preference():
            preference = applicant.preference
        else:
            preference = MajorPreference()
            
        preference.majors = major_ranks

        preference.applicant = applicant
        preference.save()
        applicant.add_related_model('major_preference',
                                    save=True,
                                    smart=True)

        return (True, major_ranks, None)

    return (False, major_ranks, errors)


def handle_education_form(request, old_education):
    applicant = request.applicant
    form = EducationForm(request.POST, 
                         instance=old_education)

    if form.is_valid():
        applicant_education = form.save(commit=False)
        applicant_education.applicant = applicant
        applicant_education.save()
        applicant.add_related_model('educational_info',
                                    save=True,
                                    smart=True)

        return (True, form)
    else:
        return (False, form)

