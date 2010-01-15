# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from django import forms

from commons.decorators import submitted_applicant_required
from commons.models import Log

from models import AdmissionMajorPreference

def get_higher_ranked_majors(majors, current_major):
    result = []
    for m in majors:
        if m.id != current_major.id:
            result.append(m)
        else:
            return result
        

def check_form_submission(post_data, higher_majors):
    if (('pref_type' not in post_data) or
        (post_data['pref_type'] not in ['no_move',
                                        'move_up_inclusive',
                                        'move_up_strict',
                                        'withdrawn'])):
        return False, 'เลือกประเภทการพิจารณาไม่ถูกต้อง, กรุณาเลือก 1 ข้อ'
    if post_data['pref_type'] in ['move_up_strict', 'move_up_inclusive']:
        mcount = len(higher_majors)
        for i in range(mcount):
            if ('major-accepted-' + str(i+1)) in post_data:
                return True, ''
        return False, 'กรุณาเลือกสาขาที่ต้องการให้พิจารณาเลื่อนอันดับอย่างน้อย 1 สาขา'
    return True, ''

def update_admission_major_preference(pref, applicant,
                                      preferred_majors,
                                      higher_majors,
                                      post_data):
    if not pref:
        pref = AdmissionMajorPreference()
        pref.applicant = applicant
    
    alist = [0] * len(preferred_majors)
    if post_data['pref_type'] in ['move_up_inclusive', 'move_up_strict']:
        for i in range(len(higher_majors)):
            if ('major-accepted-' + str(i+1)) in post_data:
                alist[i] = 1
    if post_data['pref_type'] in ['no_move', 'move_up_inclusive']:
        alist[len(higher_majors)] = 1    # current admitted major

    pref.is_accepted_list = alist
    return pref

@submitted_applicant_required
def pref(request):
    applicant = request.applicant
    admitted = False
    if applicant.has_admission_result():
        admitted = applicant.admission_result.is_admitted

    if not admitted:
        raise Http404

    admission_result = applicant.admission_result

    preferred_majors = applicant.preference.get_major_list()
    higher_majors = get_higher_ranked_majors(preferred_majors, 
                                             admission_result.admitted_major)

    
    try:
        admission_pref = applicant.admission_major_preference
    except:
        admission_pref = None

    if admission_pref:
        pref_type = admission_pref.get_pref_type()
        accepted_major_ids = [m.id for m in admission_pref.get_accepted_majors()]
        is_accepted_list = [(m.id in accepted_major_ids)
                            for m in higher_majors]
    else:
        pref_type = AdmissionMajorPreference.PrefType.new_empty()
        try:
            is_accepted_list = [False] * len(higher_majors)
        except:
            Log.create("Error: empty higher majors: %d" % (applicant.id,))
            raise

    form_check_message = ''

    if request.method=='POST':
        if 'submit' in request.POST:
            check_result, form_check_message = check_form_submission(request.POST, higher_majors)
            if check_result:
                admission_pref = update_admission_major_preference(
                    admission_pref,
                    applicant, preferred_majors,
                    higher_majors, request.POST)
                admission_pref.save()
                request.session['notice'] = 'เก็บข้อมูลการยืนยันอันดับการเลือกสาขาวิชาแล้ว'

                Log.create("confirmation - from: %s,type: %d (%s), val: %s" %
                           (request.META['REMOTE_ADDR'],
                            admission_pref.get_pref_type().ptype,
                            request.POST['pref_type'],
                            str(admission_pref.is_accepted_list)),
                           applicant_id=applicant.id,
                           applicantion_id=applicant.submission_info.applicantion_id)

                return HttpResponseRedirect(reverse('status-index'))
        else:
            if admission_pref:
                request.session['notice'] = 'ยกเลิกการแก้ไขอันดับการเลือกสาขาวิชา'
            else:
                request.session['notice'] = 'ยกเลิกการยืนยันอันดับการเลือกสาขาวิชา'

            Log.create("confirmation: cancel",
                       applicant_id=applicant.id,
                       applicantion_id=applicant.submission_info.applicantion_id)

            return HttpResponseRedirect(reverse('status-index'))
    else:
        pass

    return render_to_response('confirmation/pref.html',
                              { 'applicant': applicant,
                                'admission_result': admission_result,
                                'higher_majors': higher_majors,
                                'majors_with_is_accepted':
                                    zip(higher_majors, is_accepted_list),
                                'admission_pref': admission_pref,
                                'pref_type': pref_type,
                                'form_check_message': form_check_message })

