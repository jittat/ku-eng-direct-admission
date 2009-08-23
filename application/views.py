# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.core.urlresolvers import reverse
from models import Applicant

INDEX_PAGE = 'start-page'

def index(request):
    return render_to_response('application/index.html')

def start(request):
    return render_to_response('application/start.html')

def redirect_to_index():
    return HttpResponseRedirect(reverse(INDEX_PAGE))

FORM_STEPS = [
    'ข้อมูลส่วนตัวผู้สมัคร',
    'ที่อยู่',
    'ข้อมูลการศึกษา',
    'เลือกอันดับสาขาวิชา',
    'เลือกวิธีการส่งหลักฐาน',
    ]

class ApplicantCoreForm(forms.ModelForm):
    email_confirmation = forms.EmailField()
    class Meta:
        model = Applicant

def applicant_core_info(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect_to_index()
        
        form = ApplicantCoreForm(request.POST)
        if form.is_valid():
            if (form.cleaned_data['email'] == 
                form.cleaned_data['email_confirmation']):
                applicant = form.save()
            else:
                print 'Email error!'
                pass
    else:
        form = ApplicantCoreForm()
    return render_to_response('application/core.html', 
                              { 'form': form,
                                'steps': FORM_STEPS, 
                                'current_step': 0 })


