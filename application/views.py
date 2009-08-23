# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.forms import ModelForm

from models import Applicant

def index(request):
    return render_to_response('application/index.html')

FORM_STEPS = [
    'ข้อมูลส่วนตัวผู้สมัคร',
    'ที่อยู่',
    'ข้อมูลการศึกษา',
    'เลือกอันดับสาขาวิชา',
    'เลือกวิธีการส่งหลักฐาน',
    ]

class ApplicantCoreForm(ModelForm):
    class Meta:
        model = Applicant

def applicant_core_info(request):
    if request.method == 'POST':
        form = ApplicantCoreForm(request.POST)
        if form.is_valide():
            applicant = form.save()
    else:
        form = ApplicantCoreForm()
    return render_to_response('application/core.html', 
                              { 'form': form,
                                'step_descriptions': FORM_STEPS, 
                                'step_number': 0 })


