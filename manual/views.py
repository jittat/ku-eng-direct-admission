# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from commons.local import APP_TITLE_FORM_CHOICES

from application.models import Applicant
from application.forms import RegistrationForm, PersonalInfoForm
from application.forms.handlers import handle_personal_info_form
from application.forms.handlers import handle_address_form
from commons.utils import random_string

class NewAppForm(forms.Form):
    title = forms.ChoiceField(choices=APP_TITLE_FORM_CHOICES)
    first_name = forms.CharField(label=u'ชื่อ')
    last_name = forms.CharField(label=u'นามสกุล')
    email = forms.EmailField(label=u'อีเมล์')

    def get_applicant(self):
        return Applicant(title=self.cleaned_data['title'],
                         first_name=self.cleaned_data['first_name'],
                         last_name=self.cleaned_data['last_name'],
                         email=self.cleaned_data['email'])

def set_notice_message(request, notice):
    request.session['notice'] = notice

def get_notice_message_and_clear(request):
    if 'notice' in request.session:
        notice = request.session['notice']
        del request.session['notice']
        return notice
    else:
        return ''

@login_required
def index(request):
    notice = get_notice_message_and_clear(request)

    active_applicants = Applicant.get_active_offline_applicant()

    new_app_form = NewAppForm()

    return render_to_response("manual/index.html",
                              { 'notice': notice,
                                'active_applicants': active_applicants,
                                'form': new_app_form })

@login_required
def create(request):
    if request.method!='POST':
        return HttpResponseRedirect(reverse('manual-index'))
    new_app_form = NewAppForm(request.POST)
    if new_app_form.is_valid():
        applicant = new_app_form.get_applicant()
        applicant.random_password(20)
        # prefix email to prevent e-mail index crash
        applicant.email = "%s-%s" % (random_string(5),applicant.email)

        applicant.is_offline = True

        try:
            applicant.save()

        except IntegrityError:
            # shouldn't happen!
            set_notice_message(request,'ไม่สามารถสร้างได้เนื่องจากอีเมล์ซ้ำ')
            return HttpResponseRedirect(reverse('manual-index'))

        return HttpResponseRedirect(reverse('manual-personal',
                                            args=[applicant.id]))
    
    set_notice_message(request,'ไม่สามารถสร้างได้เนื่องจากข้อมูลผิดพลาด')
    return HttpResponseRedirect(reverse('manual-index'))


@login_required
def personal_form(request,applicant_id):
    applicant = get_object_or_404(Applicant,pk=applicant_id)
    old_info = applicant.get_personal_info_or_none()
    result, form = handle_personal_info_form(request, old_info, applicant)
    if result:
        return HttpResponseRedirect(reverse('manual-address',
                                            args=[applicant.id]))
    return render_to_response('manual/personal.html',
                              { 'applicant': applicant,
                                'form': form })

@login_required
def address_form(request, applicant_id):
    applicant = get_object_or_404(Applicant,pk=applicant_id)
    result, hform, cform = handle_address_form(request, applicant)
    if result:
        return HttpResponseRedirect(reverse('manual-edu',
                                            args=[applicant.id]))

    return render_to_response('manual/address.html', 
                              { 'applicant': applicant,
                                'home_address_form': hform,
                                'contact_address_form': cform })
