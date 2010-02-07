# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from commons.decorators import submitted_applicant_required
from commons.utils import admission_major_pref_deadline_passed
from commons.models import Log
from application.models import Applicant, SubmissionInfo

from models import AdmissionMajorPreference, AdmissionConfirmation

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

    # check for deadline
    if admission_major_pref_deadline_passed():
        return render_to_response('confirmation/pref_deadline_passed.html')

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

def get_best_scores(applicant):
    try:
        niets_scores = applicant.NIETS_scores
    except:
        return None

    return niets_scores.get_best_test_scores()

def render_confirmed_applicant(applicant):
    admission_result = applicant.admission_result
    preferred_majors = applicant.preference.get_major_list()
    higher_majors = get_higher_ranked_majors(preferred_majors, 
                                             admission_result.admitted_major)
    best_scores = get_best_scores(applicant)

    admission_pref = applicant.admission_major_preference
    pref_type = admission_pref.get_pref_type()
    accepted_major_ids = [m.id for m in admission_pref.get_accepted_majors()]
    is_accepted_list = [(m.id in accepted_major_ids)
                        for m in higher_majors]
     
    return render_to_response('confirmation/show_confirmed.html',
                              { 'applicant': applicant,
                                'best_scores': best_scores,
                                'admission_result': admission_result,
                                'higher_majors': higher_majors,
                                'majors_with_is_accepted':
                                    zip(higher_majors, is_accepted_list),
                                'admission_pref': admission_pref,
                                'pref_type': pref_type })


def render_unconfirmed_applicant(applicant):
    admission_result = applicant.admission_result
    preferred_majors = applicant.preference.get_major_list()
    higher_majors = get_higher_ranked_majors(preferred_majors, 
                                             admission_result.admitted_major)
    best_scores = get_best_scores(applicant)
    return render_to_response('confirmation/show_unconfirmed.html',
                              { 'applicant': applicant,
                                'best_scores': best_scores,
                                'admission_result': admission_result,
                                'higher_majors': higher_majors })

@login_required
def interview_info(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    try:
        pref = applicant.admission_major_preference
    except:
        pref = None

    if pref:
        return render_confirmed_applicant(applicant)
    else:
        return render_unconfirmed_applicant(applicant)


@login_required
def index(request):
    confirmations = AdmissionConfirmation.objects.select_related(depth=1).all()[:20]

    confirmation_count = AdmissionConfirmation.objects.count()

    stat = { 'total': confirmation_count }

    if 'notice' in request.session:
        notice = request.session['notice']
        del request.session['notice']
    else:
        notice = ''

    return render_to_response('confirmation/index.html',
                              { 'confirmations': confirmations,
                                'stat': stat,
                                'notice': notice })


@login_required
def confirm(request, preview=False):
    if request.method != 'POST':
        return HttpResponseForbidden()
    if not request.user.has_perm('confirmation.add_admissionconfirmation'):
        return HttpResponseForbidden('ขออภัยคุณไม่มีสิทธิ์ในการทำรายการดังกล่าว')

    if 'cancel' in request.POST:
        request.session['notice'] = u'ยกเลิกการทำรายการ'
        return HttpResponseRedirect(reverse('confirmation-index'))

    import re

    if (('application_id' not in request.POST) or
        (not re.match(r'53[123]\d{5}', request.POST['application_id']))):
        request.session['notice'] = u'เกิดข้อผิดพลาด หมายเลขประจำตัวผู้สมัครไม่ถูกต้อง'
        return HttpResponseRedirect(reverse('confirmation-index'))

    application_id = request.POST['application_id']
    submission_info = SubmissionInfo.find_by_ticket_number(application_id)
    if submission_info==None:
        request.session['notice'] = (u'เกิดข้อผิดพลาด ไม่พบผู้สมัครที่ใช้หมายเลข %s' % application_id)
        return HttpResponseRedirect(reverse('confirmation-index'))

    applicant = submission_info.applicant

    if (not applicant.has_admission_result() or
        not applicant.admission_result.is_final_admitted):
        request.session['notice'] = (u'เกิดข้อผิดพลาด ผู้สมัครที่ใช้หมายเลข %s (%s) '
                                     u'ไม่ผ่านการคัดเลือกเข้าศึกษาต่อ' % 
                                     (application_id, applicant.full_name()))
        return HttpResponseRedirect(reverse('confirmation-index'))


    try:
        if applicant.admission_confirmation!=None:
            request.session['notice'] = (u'เกิดข้อผิดพลาด ผู้สมัครที่ใช้หมายเลข %s (%s) '
                                         u'ได้ยืนยันสิทธิ์แล้ว ถ้าต้องการยกเลิกกรุณาแจ้งผู้ดูแล' % 
                                         (application_id, applicant.full_name()))
            return HttpResponseRedirect(reverse('confirmation-index'))            
    except:
        pass

    if preview:
        return render_to_response('confirmation/preview.html',
                                  { 'applicant': applicant })
    else:
        confirmation = AdmissionConfirmation(applicant=applicant,
                                             confirming_user=request.user)

        Log.create("admission confirmation - from: %s" %
                   (request.META['REMOTE_ADDR'],),
                   user=request.user.username,
                   applicant_id=applicant.id,
                   applicantion_id=application_id)

        try:
            confirmation.save()
        except:
            Log.create("ERROR: admission confirmation - from: %s" %
                       (request.META['REMOTE_ADDR'],),
                       user=request.user.username,
                       applicant_id=applicant.id,
                       applicantion_id=application_id)

            request.session['notice'] = u'เกิดข้อผิดพลาดในการยืนยันสิทธิ์ กรุณาแจ้งผู้ดูแลด่วน'
            return HttpResponseRedirect(reverse('confirmation-index'))            

        request.session['notice'] = u'บันทึกการยืนยันสิทธิ์เรียบร้อย ชื่อผู้ยืนยันควรปรากฏในตารางด้านล่าง'
        return HttpResponseRedirect(reverse('confirmation-index'))            


def render_confirmation_form_second_round(request, applicant):
    second_round_admitted = False
    if applicant.has_admission_result():
        second_round_admitted = (applicant.admission_result.is_final_admitted and (not applicant.admission_result.is_admitted))

    if not second_round_admitted:
        raise Http404

    admission_result = applicant.admission_result

    Log.create("view confirmation second round - id: %d, from: %s" %
               (applicant.id, request.META['REMOTE_ADDR']),
               applicant_id=applicant.id,
               applicantion_id=applicant.submission_info.applicantion_id)

    return render_to_response('confirmation/second_round_confirmation.html',
                              { 'applicant': applicant,
                                'admission_result': admission_result })


@submitted_applicant_required
def show_confirmation_second_round(request):
    applicant = request.applicant
    return render_confirmation_form_second_round(request, applicant)

@login_required
def admin_show_confirmation_second_round(request, app_id):
    applicant = get_object_or_404(Applicant, pk=app_id)
    return render_confirmation_form_second_round(request, applicant)
