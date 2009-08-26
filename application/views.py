# -*- coding: utf-8 -*-
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.core.urlresolvers import reverse

from decorators import applicant_required
from models import Applicant, ApplicantAccount
from models import Address, ApplicantAddress, Education
from utils import redirect_to_index

def index(request):
    return render_to_response('application/index.html')

def start(request):
    return render_to_response('application/start.html')

FORM_STEPS = [
    'ข้อมูลส่วนตัวผู้สมัคร',
    'ที่อยู่',
    'ข้อมูลการศึกษา',
    'เลือกอันดับสาขาวิชา',
    'เลือกวิธีการส่งหลักฐาน',
    ]

def validate_phone_number(phone_number):
    # TODO: describe ext format in web form
    return re.match(u'^([0-9\\- #]|ต่อ|ext)+$', phone_number) != None

class ApplicantCoreForm(forms.ModelForm):
    email_confirmation = forms.EmailField()

    def clean_national_id(self):
        if re.match(r'^(\d){13}$',self.cleaned_data['national_id']) == None:
            raise forms.ValidationError("รหัสประจำตัวประชาชนไม่ถูกต้อง")
        return self.cleaned_data['national_id']

    def clean_phone_number(self):
        if not validate_phone_number(self.cleaned_data['phone_number']):
            raise forms.ValidationError("หมายเลขโทรศัพท์ไม่ถูกต้อง")
        return self.cleaned_data['phone_number']

    def clean_email_confirmation(self):
        if (self.cleaned_data['email'] !=
            self.cleaned_data['email_confirmation']):
            raise forms.ValidationError("อีเมล์ที่ระบุไม่ตรงกัน")
        return self.cleaned_data['email_confirmation']

    class Meta:
        model = Applicant

def applicant_core_info(request):
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
        form = ApplicantCoreForm()
    return render_to_response('application/core.html', 
                              { 'form': form,
                                'steps': FORM_STEPS, 
                                'current_step': 0 })


class AddressForm(forms.ModelForm):
    # TODO: add form validation
    class Meta:
        model = Address

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


class EducationForm(forms.ModelForm):
    # TODO: add form validation
    class Meta:
        model = Education
        exclude = ['applicant']

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
            return HttpResponseRedirect(reverse('apply-doc-menu'))
            
    else:
        form = EducationForm(instance=old_education)

    return render_to_response('application/education.html', 
                              { 'form': form,
                                'steps': FORM_STEPS, 
                                'current_step': 2 })

@applicant_required
def applicant_doc_menu(request):
    return render_to_response('application/doc_menu.html')

