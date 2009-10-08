# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django import forms

from commons.utils import redirect_to_index

from application.models import Applicant, ApplicantAccount
from application.forms import LoginForm, ForgetPasswordForm

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
                applicant.applicantaccount.check_password(passwd)):
                # authenticated

                request.session['applicant_id'] = applicant.id

                return HttpResponseRedirect(reverse('apply-core'))
            
            error_messages.append(u"รหัสผ่านไม่ถูกต้อง")
    else:
        form = LoginForm()
    return render_to_response('application/login.html',
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


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']['email']
            applicant = form.cleaned_data['email']['applicant']
            account = applicant.applicantaccount
            new_pwd = account.random_password()
            account.save()
            send_applicant_email(applicant, new_pwd)
            
            return HttpResponseRedirect(reverse('apply-login'))
    else:
        form = ForgetPasswordForm()

    return render_to_response('application/forget.html', 
                              { 'form': form })


    
