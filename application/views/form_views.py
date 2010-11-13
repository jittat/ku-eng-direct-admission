# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django import forms

from commons.decorators import applicant_required
from commons.decorators import active_applicant_required
from commons.decorators import active_applicant_required_or_update
from commons.utils import redirect_to_index
from commons.email import send_submission_confirmation_by_email

from application.decorators import init_applicant
from commons.decorators import within_submission_deadline
from commons.utils import submission_deadline_passed, redirect_to_deadline_error

from application.models import Applicant
from application.models import PersonalInfo
from application.models import Address, ApplicantAddress, Education
from application.models import Major, MajorPreference

from application.forms import PersonalInfoForm, AddressForm, EducationForm, SingleMajorPreferenceForm
from application.forms.handlers import handle_major_form
from application.forms.handlers import assign_major_pref_to_applicant
from application.forms.handlers import handle_education_form
from application.forms.handlers import handle_personal_info_form
from application.forms.handlers import handle_address_form


def build_form_step_dict(form_steps):
    d = {}
    s = 0
    for name,url_name in form_steps:
        d[url_name] = s
        s += 1
    return d

# a list of tuples (form name, url-name).
FORM_STEPS = [
    ('ข้อมูลส่วนตัวผู้สมัคร','apply-personal-info'),
    ('ที่อยู่','apply-address'),
    ('ข้อมูลการศึกษา','apply-edu'),
    ('อันดับสาขาวิชา','apply-majors'),
    ('ยืนยันข้อมูล','apply-confirm'),
    ]

FORM_STEP_DICT = build_form_step_dict(FORM_STEPS)

def get_allowed_form_steps(applicant):
    if applicant==None:
        return FORM_STEP_DICT['apply-personal-info']
    if applicant.has_major_preference():
        return FORM_STEP_DICT['apply-confirm']
    if applicant.has_educational_info():
        return FORM_STEP_DICT['apply-majors']
    if applicant.has_address():
        return FORM_STEP_DICT['apply-edu']
    if applicant.has_personal_info():
        return FORM_STEP_DICT['apply-address']
    return FORM_STEP_DICT['apply-personal-info']

def build_form_step_info(current_step, applicant):
    return { 'steps': FORM_STEPS,
             'current_step': current_step,
             'max_linked_step': get_allowed_form_steps(applicant) }

def redirect_to_first_form():
    if not submission_deadline_passed():
        return HttpResponseRedirect(reverse(FORM_STEPS[0][1]))
    else:
        return redirect_to_deadline_error()


def redirect_to_applicant_first_page(applicant):
    """
    takes the applicant, and depending on the submission status, take
    the applicant to the right page.  The condition is as follows:

    - if the applicant has not submitted the information form, take
      the applicant to the first form.

    - if the applicant has already submitted everything, take the
      applicant to the status page.

    TODO: doc_menu for applicant that start submitting docs, but not
    complete.
    """
    if not applicant.is_submitted:
        return redirect_to_first_form()
    else:
        return HttpResponseRedirect(reverse('status-index'))

@within_submission_deadline
@active_applicant_required
def applicant_personal_info(request):
    applicant = request.applicant
    old_info = applicant.get_personal_info_or_none()
    result, form = handle_personal_info_form(request, old_info)

    if result:
        return HttpResponseRedirect(reverse('apply-address'))

    form_step_info = build_form_step_info(0,applicant)
    return render_to_response('application/personal.html',
                              { 'applicant': applicant,
                                'form': form,
                                'form_step_info': form_step_info })

@within_submission_deadline
@active_applicant_required
def applicant_address(request):
    result, hform, cform = handle_address_form(request)
    if result:
        return HttpResponseRedirect(reverse('apply-edu'))

    form_step_info = build_form_step_info(1,request.applicant)
    return render_to_response('application/address.html', 
                              { 'home_address_form': hform,
                                'contact_address_form': cform,
                                'form_step_info': form_step_info })


@within_submission_deadline
@active_applicant_required
def applicant_education(request):
    applicant = request.applicant
    old_education = applicant.get_educational_info_or_none()
    result, form = handle_education_form(request, old_education)
    if result:
        return HttpResponseRedirect(reverse('apply-majors'))

    accept_only_graduated = settings.ACCEPT_ONLY_GRADUATED

    form_step_info = build_form_step_info(2,applicant)
    return render_to_response('application/education.html', 
                              { 'form': form,
                                'accept_only_graduated': accept_only_graduated,
                                'form_step_info': form_step_info })


def applicant_major_single_choice(request):
    applicant = request.applicant

    if (request.method == 'POST') and ('cancel' not in request.POST):

        form = SingleMajorPreferenceForm(request.POST)
        if form.is_valid():
            assign_major_pref_to_applicant(applicant,
                                           [form.cleaned_data['major'].number])
            return HttpResponseRedirect(reverse('apply-doc-menu'))
    else:
        prev_major = None
        if applicant.has_major_preference():
            pref = applicant.preference.majors
            if len(pref)==0:
                prev_major = None
            else:
                majors = dict([(int(m.number), m) for m in Major.get_all_majors()])
                prev_major = majors[pref[0]]
        if prev_major!=None:
            form = SingleMajorPreferenceForm(initial={'major': prev_major.id})
        else:
            form = SingleMajorPreferenceForm()

    # add step info
    form_data = {}
    form_step_info = build_form_step_info(3, applicant)
    form_data['form_step_info'] = form_step_info
    form_data['form'] = form
    return render_to_response('application/majors_single.html',
                              form_data)


def prepare_major_form(applicant, pref_ranks=None, errors=None):
    majors = Major.get_all_majors()
    max_major_rank = settings.MAX_MAJOR_RANK

    if pref_ranks==None:
        pref_ranks = [None] * len(majors) 

    ranks = [i+1 for i in range(max_major_rank)]

    return { 'majors_prefs': zip(majors,pref_ranks),
             'ranks': ranks,
             'max_major_rank': max_major_rank,
             'errors': errors }


@within_submission_deadline
@active_applicant_required
def applicant_major(request):
    if settings.MAX_MAJOR_RANK == 1:
        return applicant_major_single_choice(request)

    applicant = request.applicant

    if (request.method == 'POST') and ('cancel' not in request.POST):

        result, major_list, errors = handle_major_form(request)

        if result:
            return HttpResponseRedirect(reverse('apply-confirm'))

        pref_ranks = MajorPreference.major_list_to_major_rank_list(major_list)
        form_data = prepare_major_form(applicant, pref_ranks, errors)

    else:
        if applicant.has_major_preference():
            pref_ranks = applicant.preference.to_major_rank_list()
        else:
            pref_ranks = None

        form_data = prepare_major_form(applicant, pref_ranks)

    # add step info
    form_step_info = build_form_step_info(3, applicant)
    form_data['form_step_info'] = form_step_info
    return render_to_response('application/majors.html',
                              form_data)


@within_submission_deadline
@active_applicant_required
def applicant_doc_menu(request):
    return HttpResponseForbidden()


    if settings.FORCE_UPLOAD_DOC:
        return HttpResponseRedirect(reverse('upload-index'))

    applicant = request.applicant
    chosen = applicant.doc_submission_method != Applicant.UNDECIDED_METHOD
    #print applicant, chosen
    form_step_info = build_form_step_info(4,applicant)
    return render_to_response('application/doc_menu.html',
                              {'form_step_info': form_step_info,
                               'applicant': applicant,
                               'chosen': chosen })


@within_submission_deadline
@active_applicant_required
def info_confirm(request):
    if settings.FORCE_UPLOAD_DOC:
        return HttpResponseRedirect(reverse('upload-index'))

    applicant = request.applicant

    if request.method == 'POST':
        if 'submit' in request.POST:
            return HttpResponseRedirect(reverse('apply-conditions'))
        else:
            return render_to_response('application/submission/not_submitted.html')

    return render_to_response('application/confirm.html',
                              {'applicant': applicant })
    

@within_submission_deadline
@active_applicant_required
def applicant_conditions(request):
    applicant = request.applicant

    if request.method == 'POST':
        if 'submit' in request.POST:
            try:
                applicant.submit(Applicant.SUBMITTED_ONLINE)
            except Applicant.DuplicateSubmissionError:
                return render_to_response(
                    'commons/submission_already_submitted.html',
                    { 'applicant': applicant })

            send_submission_confirmation_by_email(applicant)
            return HttpResponseRedirect(reverse('apply-success'))
        else:
            return render_to_response('application/submission/not_submitted.html')

    return render_to_response('application/conditions.html',
                              {'applicant': applicant })
    

@applicant_required
def submission_success(request):
    if not request.applicant.is_submitted:
        return render_to_response('application/submission/ticket_not_submitted.html')

    return render_to_response('application/submission/success.html',
                              {'applicant': request.applicant})

@applicant_required
def submission_ticket(request):
    if not request.applicant.is_submitted:
        return render_to_response('application/submission/ticket_not_submitted.html')

    amount = 350
    amount_str = u'สามร้อยห้าสิบบาทถ้วน'

    verification = request.applicant.verification_number()
    return render_to_response('application/payin/ticket.html',
                              {'amount': amount,
                               'amount_str': amount_str,
                               'applicant': request.applicant,
                               'verification': verification })
        
    
