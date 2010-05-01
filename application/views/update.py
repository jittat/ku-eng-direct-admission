# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings

from commons.decorators import submitted_applicant_required
from commons.decorators import within_submission_deadline
from commons.utils import submission_deadline_passed, redirect_to_deadline_error

from application.views.form_views import prepare_major_form
from application.forms.handlers import handle_major_form
from application.forms.handlers import assign_major_pref_to_applicant
from application.forms.handlers import handle_education_form
from application.forms import EducationForm, SingleMajorPreferenceForm
from application.models import Applicant, MajorPreference, Major

from commons.email import send_sub_method_change_notice_by_email

def update_major_single_choice(request):
    applicant = request.applicant

    if request.method == 'POST':

        if 'cancel' not in request.POST:
            form = SingleMajorPreferenceForm(request.POST)
            if form.is_valid():
                assign_major_pref_to_applicant(applicant,
                                               [form.cleaned_data['major'].number])
                request.session['notice'] = 'การแก้ไขอันดับสาขาวิชาเรียบร้อย'
                return HttpResponseRedirect(reverse('status-index'))
        else:
            request.session['notice'] = 'อันดับสาขาวิชาไม่ถูกแก้ไข'
            return HttpResponseRedirect(reverse('status-index'))

    else:
        if applicant.has_major_preference():
            pref = applicant.preference.majors
            if len(pref)==0:
                prev_major = None
            else:
                majors = dict([(int(m.number), m) for m in Major.get_all_majors()])
                prev_major = majors[pref[0]]
        form = SingleMajorPreferenceForm(initial={'major': prev_major.id})

    # add step info
    form_data = {}
    form_data['step_name'] = 'แก้ไขอันดับสาขาวิชา'
    form_data['can_log_out'] = True
    form_data['form'] = form
    return render_to_response('application/update/majors_single.html',
                              form_data)
    

@within_submission_deadline
@submitted_applicant_required
def update_majors(request):
    if settings.MAX_MAJOR_RANK == 1:
        return update_major_single_choice(request)

    applicant = request.applicant

    if request.method == 'POST': 

        if 'cancel' not in request.POST:

            result, major_list, errors = handle_major_form(request)

            if result:
                request.session['notice'] = 'การแก้ไขอันดับสาขาวิชาเรียบร้อย'
                return HttpResponseRedirect(reverse('status-index'))

        else:
            request.session['notice'] = 'อันดับสาขาวิชาไม่ถูกแก้ไข'
            return HttpResponseRedirect(reverse('status-index'))

        pref_ranks = MajorPreference.major_list_to_major_rank_list(major_list)
        form_data = prepare_major_form(applicant, pref_ranks, errors)

    else:
        if applicant.has_major_preference():
            pref_ranks = applicant.preference.to_major_rank_list()
        else:
            pref_ranks = [None] * len(majors)

        form_data = prepare_major_form(applicant, pref_ranks)

    # add step info
    form_data['step_name'] = 'แก้ไขอันดับสาขาวิชา'
    form_data['can_log_out'] = True
    return render_to_response('application/update/majors.html',
                              form_data)

@within_submission_deadline
@submitted_applicant_required
def update_education(request):
    applicant = request.applicant
    if not applicant.submission_info.can_update_info():
        return HttpResponseRedirect(reverse('status-index'))
        
    old_education = applicant.get_educational_info_or_none()

    result, form = handle_education_form(request, old_education)

    if result:
        request.session['notice'] = 'การแก้ไขข้อมูลการศึกษาเรียบร้อย'
        return HttpResponseRedirect(reverse('status-index'))
    elif 'cancel' in request.POST:
        request.session['notice'] = 'ข้อมูลการศึกษาไม่ถูกแก้ไข'
        return HttpResponseRedirect(reverse('status-index'))

    return render_to_response('application/update/education.html',
                              {'form': form,
                               'can_log_out': True,
                               'applicant': applicant })


@within_submission_deadline
@submitted_applicant_required
def update_to_postal_submission(request):

    applicant = request.applicant

    if request.method == 'POST': 

        if 'cancel' not in request.POST:

            submission_info = applicant.submission_info
            submission_info.delete()

            applicant.doc_submission_method = Applicant.UNDECIDED_METHOD
            applicant.is_submitted = False
            applicant.save()

            request.session['notice'] = 'คุณได้ยกเลิกการเลือกส่งหลักฐานทางไปรษณีย์แล้ว  อย่าลืมว่าคุณจะต้องยืนยันข้อมูลอีกครั้ง'

            send_sub_method_change_notice_by_email(applicant)

            return HttpResponseRedirect(reverse('upload-index'))

        else:
            request.session['notice'] = 'วิธีการส่งยังคงเป็นแบบไปรษณีย์ไม่เปลี่ยนแปลง'
            return HttpResponseRedirect(reverse('status-index'))

    else:
        return render_to_response('application/update/postal_sub.html',
                                  { 'can_log_out': False,
                                    'applicant': applicant })

