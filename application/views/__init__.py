# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django import forms

from commons.decorators import applicant_required
from commons.utils import redirect_to_index
from application.decorators import init_applicant

from application.models import Applicant, ApplicantAccount
from application.models import Address, ApplicantAddress, Education
from application.models import Major, MajorPreference

from application.forms import ApplicantCoreForm, AddressForm, EducationForm

from application.email import send_applicant_email


def build_form_step_dict(form_steps):
    d = {}
    s = 0
    for name,url_name in form_steps:
        d[url_name] = s
        s += 1
    return d

# a list of tuples (form name, url-name).
FORM_STEPS = [
    ('ข้อมูลส่วนตัวผู้สมัคร','apply-core'),
    ('ที่อยู่','apply-address'),
    ('ข้อมูลการศึกษา','apply-edu'),
    ('อันดับสาขาวิชา','apply-majors'),
    ('หลักฐานการสมัคร','apply-doc-menu'),
    ]

FORM_STEP_DICT = build_form_step_dict(FORM_STEPS)

def get_allowed_form_steps(applicant):
    if applicant==None:
        return FORM_STEP_DICT['apply-core']
    if applicant.has_major_preference():
        return FORM_STEP_DICT['apply-doc-menu']
    if applicant.has_educational_info():
        return FORM_STEP_DICT['apply-majors']
    if applicant.has_address():
        return FORM_STEP_DICT['apply-edu']
    if applicant.id != None:
        return FORM_STEP_DICT['apply-address']
    return FORM_STEP_DICT['apply-core']

def build_form_step_info(current_step, applicant):
    return { 'steps': FORM_STEPS,
             'current_step': current_step,
             'max_linked_step': get_allowed_form_steps(applicant) }

@init_applicant
def applicant_core_info(request):
    applicant = request.applicant
    if applicant != None:
        old_email = applicant.email
    else:
        old_email = ''

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect_to_index(request)
        
        form = ApplicantCoreForm(request.POST)
        if form.is_valid():
            applicant = form.save()

            account = ApplicantAccount(applicant=applicant)
            new_pwd = account.random_password()
            account.save()

            send_applicant_email(applicant, new_pwd)

            request.session['applicant_id'] = applicant.id

            return HttpResponseRedirect(reverse('apply-address'))
    else:
        form = ApplicantCoreForm(instance=applicant,
                                 initial={'email_confirmation': old_email})

    form_step_info = build_form_step_info(0,applicant)
    return render_to_response('application/core.html', 
                              { 'form': form,
                                'form_step_info': form_step_info })

@applicant_required
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

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect_to_index(request)

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


@applicant_required
def applicant_education(request):
    applicant = request.applicant

    if applicant.has_educational_info():
        old_education = applicant.education
        old_education.fix_boolean_fields()
    else:
        old_education = None

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect_to_index(request)

        form = EducationForm(request.POST, 
                                       instance=old_education)

        if form.is_valid():
            applicant_education = form.save(commit=False)
            applicant_education.applicant = applicant
            applicant_education.save()
            return HttpResponseRedirect(reverse('apply-majors'))
            
    else:
        form = EducationForm(instance=old_education)

    form_step_info = build_form_step_info(2,applicant)
    return render_to_response('application/education.html', 
                              { 'form': form,
                                'form_step_info': form_step_info })


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

@applicant_required
def applicant_major(request):
    applicant = request.applicant

    majors = Major.get_all_majors()

    if applicant.has_major_preference():
        old_preference = applicant.preference
        pref_ranks = old_preference.to_major_rank_list()
    else:
        old_preference = None
        pref_ranks = [None] * len(majors)

    max_major_rank = settings.MAX_MAJOR_RANK
    ranks = [i+1 for i in range(max_major_rank)]
    if request.method == 'POST':
        print extract_ranks(request.POST, majors)

        if old_preference!=None:
            preference = old_preference
        else:
            preference = MajorPreference()

        preference.majors = extract_ranks(request.POST, majors)
        preference.applicant = applicant
        preference.save()

        return HttpResponseRedirect(reverse('apply-doc-menu'))

    form_step_info = build_form_step_info(3,applicant)
    return render_to_response('application/majors.html',
                              { 'majors_prefs': zip(majors,pref_ranks),
                                'ranks': ranks,
                                'max_major_rank': max_major_rank,
                                'form_step_info': form_step_info })

@applicant_required
def applicant_doc_menu(request):
    applicant = request.applicant
    chosen = applicant.doc_submission_method != Applicant.UNDECIDED_METHOD
    form_step_info = build_form_step_info(4,applicant)
    return render_to_response('application/doc_menu.html',
                              {'form_step_info': form_step_info,
                               'applicant': applicant,
                               'chosen': chosen })


@applicant_required
def info_confirm(request):
    applicant = request.applicant

    if request.method == 'POST':
        if 'submit' in request.POST:
            applicant.doc_submission_method = Applicant.SUBMITTED_BY_MAIL
            applicant.is_submitted = True
            applicant.save()
            return HttpResponseRedirect(reverse('apply-ticket'))
        else:
            return render_to_response('application/submission/not_submitted.html')

    return render_to_response('application/confirm.html',
                              {'applicant': applicant })
    

@applicant_required
def submission_ticket(request):
    if not request.applicant.is_submitted:
        return render_to_response('application/submission/ticket_not_submitted.html')
    
    request.applicant.generate_submission_ticket()

    return render_to_response('application/submission/ticket.html',
                              {'applicant': request.applicant })
        
    
