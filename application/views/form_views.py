# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
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

from application.models import Applicant
from application.models import PersonalInfo
from application.models import Address, ApplicantAddress, Education
from application.models import Major, MajorPreference

from application.forms import PersonalInfoForm, AddressForm, EducationForm
from application.forms.handlers import handle_major_form

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
    ('หลักฐานการสมัคร','apply-doc-menu'),
    ]

FORM_STEP_DICT = build_form_step_dict(FORM_STEPS)

def get_allowed_form_steps(applicant):
    if applicant==None:
        return FORM_STEP_DICT['apply-personal-info']
    if applicant.has_major_preference():
        return FORM_STEP_DICT['apply-doc-menu']
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
    return HttpResponseRedirect(reverse(FORM_STEPS[0][1]))

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


@active_applicant_required
def applicant_personal_info(request):
    applicant = request.applicant

    if applicant.has_personal_info():
        old_info = applicant.personal_info
    else:
        old_info = None

    if (request.method == 'POST') and ('cancel' not in request.POST):
        form = PersonalInfoForm(request.POST, instance=old_info)
        if form.is_valid():
            personal_info = form.save(commit=False)
            personal_info.applicant = applicant
            personal_info.save()
            applicant.add_related_model('personal_info',
                                        save=True, 
                                        smart=True)

            return HttpResponseRedirect(reverse('apply-address'))
    else:
        form = PersonalInfoForm(instance=old_info)

    form_step_info = build_form_step_info(0,applicant)
    return render_to_response('application/personal.html',
                              { 'applicant': applicant,
                                'form': form,
                                'form_step_info': form_step_info })

@active_applicant_required
def applicant_address(request):
    applicant = request.applicant
    have_old_address = applicant.has_address()

    if have_old_address:
        old_applicant_address = applicant.address
        old_home_address = applicant.address.home_address
        old_contact_address = applicant.address.contact_address
    else:
        # still need this for form instances
        old_home_address, old_contact_address = None, None

    if (request.method == 'POST') and ('cancel' not in request.POST):

        home_address_form = AddressForm(request.POST, 
                                        prefix="home",
                                        instance=old_home_address)
        contact_address_form = AddressForm(request.POST, 
                                           prefix="contact",
                                           instance=old_contact_address)

        if (home_address_form.is_valid() and
            contact_address_form.is_valid()):
            home_address = home_address_form.save()
            contact_address = contact_address_form.save()

            applicant_address = ApplicantAddress(
                applicant=applicant,
                home_address=home_address,
                contact_address=contact_address)

            if have_old_address:
                applicant_address.id = old_applicant_address.id

            applicant_address.save()
            applicant.add_related_model('address',
                                        save=True,
                                        smart=True)

            return HttpResponseRedirect(reverse('apply-edu'))
    else:
        home_address_form = AddressForm(prefix="home",
                                        instance=old_home_address)
        contact_address_form = AddressForm(prefix="contact",
                                           instance=old_contact_address)

    form_step_info = build_form_step_info(1,applicant)
    return render_to_response('application/address.html', 
                              { 'home_address_form': home_address_form,
                                'contact_address_form': contact_address_form,
                                'form_step_info': form_step_info })


@active_applicant_required
def applicant_education(request):
    applicant = request.applicant

    if applicant.has_educational_info():
        old_education = applicant.education
        old_education.fix_boolean_fields()
    else:
        old_education = None

    if (request.method == 'POST') and ('cancel' not in request.POST):

        form = EducationForm(request.POST, 
                             instance=old_education)

        if form.is_valid():
            applicant_education = form.save(commit=False)
            applicant_education.applicant = applicant
            applicant_education.save()
            applicant.add_related_model('educational_info',
                                        save=True,
                                        smart=True)

            return HttpResponseRedirect(reverse('apply-majors'))
            
    else:
        form = EducationForm(instance=old_education)

    form_step_info = build_form_step_info(2,applicant)
    return render_to_response('application/education.html', 
                              { 'form': form,
                                'form_step_info': form_step_info })

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


@active_applicant_required
def applicant_major(request):
    applicant = request.applicant

    if (request.method == 'POST') and ('cancel' not in request.POST):

        result, major_list, errors = handle_major_form(request)

        if result:
            return HttpResponseRedirect(reverse('apply-doc-menu'))

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


@active_applicant_required
def applicant_doc_menu(request):
    applicant = request.applicant
    chosen = applicant.doc_submission_method != Applicant.UNDECIDED_METHOD
    #print applicant, chosen
    form_step_info = build_form_step_info(4,applicant)
    return render_to_response('application/doc_menu.html',
                              {'form_step_info': form_step_info,
                               'applicant': applicant,
                               'chosen': chosen })


@active_applicant_required
def info_confirm(request):
    applicant = request.applicant

    if request.method == 'POST':
        if 'submit' in request.POST:
            try:
                applicant.submit(Applicant.SUBMITTED_BY_MAIL)
            except Applicant.DuplicateSubmissionError:
                return render_to_response(
                    'commons/submission_already_submitted.html',
                    { 'applicant': applicant })

            send_submission_confirmation_by_email(applicant)
            return HttpResponseRedirect(reverse('apply-ticket'))
        else:
            return render_to_response('application/submission/not_submitted.html')

    return render_to_response('application/confirm.html',
                              {'applicant': applicant })
    

@applicant_required
def submission_ticket(request):
    if not request.applicant.is_submitted:
        return render_to_response('application/submission/ticket_not_submitted.html')

    verification = request.applicant.verification_number()
    return render_to_response('application/submission/success.html',
                              {'applicant': request.applicant,
                               'verification': verification })
        
    
