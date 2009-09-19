# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings

from decorators import applicant_required, init_applicant
from utils import redirect_to_index

from models import Applicant, ApplicantAccount
from models import Address, ApplicantAddress, Education
from models import Major, MajorPreference

from forms import ApplicantCoreForm, AddressForm, EducationForm

def index(request):
    return render_to_response('application/index.html')

def start(request):
    return render_to_response('application/start.html')

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

def login(request):
    error_messages = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['password']

            try:
                applicant = Applicant.objects.filter(email=email).all()[0]
            except Applicant.DoesNotExist:
                applicant = None

            if (applicant!=None and 
                applicant.applicantaccount.check_password(passwd)):
                # authenticated

                request.session['applicant_id'] = applicant.id

                return HttpResponseRedirect(reverse('apply-address'))
            
            error_messages.append(u"รหัสผ่านไม่ถูกต้อง")
    else:
        form = LoginForm()
    return render_to_response('application/login.html',
                              { 'form': form,
                                'errors': error_messages })
    

FORM_STEPS = [
    ('ข้อมูลส่วนตัวผู้สมัคร','apply-core'),
    ('ที่อยู่','apply-address'),
    ('ข้อมูลการศึกษา','apply-edu'),
    ('เลือกอันดับสาขาวิชา','apply-majors'),
    ('เลือกวิธีการส่งหลักฐาน','apply-doc-menu'),
    ]

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
            print "PASSWORD:", new_pwd
            account.save()

            request.session['applicant_id'] = applicant.id

            return HttpResponseRedirect(reverse('apply-address'))
    else:
        form = ApplicantCoreForm(instance=applicant,
                                 initial={'email_confirmation': old_email})
    return render_to_response('application/core.html', 
                              { 'form': form,
                                'steps': FORM_STEPS, 
                                'current_step': 0 })


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

    return render_to_response('application/address.html', 
                              { 'home_address_form': home_address_form,
                                'contact_address_form': contact_address_form,
                                'steps': FORM_STEPS, 
                                'current_step': 1 })


@applicant_required
def applicant_education(request):
    applicant = request.applicant

    if applicant.has_educational_info():
        old_education = applicant.education
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

    return render_to_response('application/education.html', 
                              { 'form': form,
                                'steps': FORM_STEPS, 
                                'current_step': 2 })

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

        return HttpResponseRedirect(reverse('apply-majors'))

    return render_to_response('application/majors.html',
                              { 'majors_prefs': zip(majors,pref_ranks),
                                'ranks': ranks,
                                'max_major_rank': max_major_rank,
                                'steps': FORM_STEPS,
                                'current_step': 3})

@applicant_required
def applicant_doc_menu(request):
    return render_to_response('application/doc_menu.html')

