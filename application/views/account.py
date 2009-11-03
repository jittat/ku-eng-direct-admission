# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django import forms

from commons.utils import redirect_to_index
from application.views import redirect_to_first_form

from application.models import Applicant
from application.forms import LoginForm, ForgetPasswordForm
from application.forms import RegistrationForm
from application.email import send_applicant_email

ALLOWED_LOGOUT_REDIRECTION = ['http://admission.eng.ku.ac.th']

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
                applicant.check_password(passwd)):
                # authenticated

                request.session['applicant_id'] = applicant.id

                return redirect_to_first_form()
            
            from django.forms.util import ErrorList

            form._errors['password'] = ErrorList(['รหัสผ่านผิดพลาด'])
            error_messages.append('รหัสผ่านผิดพลาด')
    else:
        form = LoginForm()
    return render_to_response('application/start.html',
                              { 'form': form,
                                'errors': error_messages })

def logout(request):
    next_url = None
    if 'url' in request.GET:
        next_url = request.GET['url']
        if next_url[0]!='/':
            next_url = 'http://' + next_url
    request.session.flush()
    if next_url and (next_url in ALLOWED_LOGOUT_REDIRECTION):
        return HttpResponseRedirect(next_url)
    else:
        return redirect_to_index(request)


def register(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect_to_index(request)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            passwd = applicant.random_password()
            applicant.save()
            send_applicant_email(applicant, passwd)
            return render_to_response('application/registration-success.html',
                                      {'email': form.cleaned_data['email']})
    else:
        form = RegistrationForm()
    return render_to_response('application/registration.html',
                              { 'form': form })

def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']['email']
            applicant = form.cleaned_data['email']['applicant']
            new_pwd = applicant.random_password()
            applicant.save()
            print applicant.email
            send_applicant_email(applicant, new_pwd)
            
            return HttpResponseRedirect(reverse('apply-login'))
    else:
        form = ForgetPasswordForm()

    return render_to_response('application/forget.html', 
                              { 'form': form })


    
