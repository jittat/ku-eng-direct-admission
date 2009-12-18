# -*- coding: utf-8 -*-
import os.path

from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.conf import settings

from commons.decorators import submitted_applicant_required
from commons.utils import extract_variable_from_session_or_none, serve_file
from commons.utils import supplement_submission_deadline_passed

from models import SupplementType, Supplement

SUPPLEMENT_TYPE_CHOICES = [(s.id, s.name) 
                           for s 
                           in SupplementType.objects.all()]
SUPPLEMENTS = dict([(s.id, s) for s in SupplementType.objects.all()])

class SupplementForm(forms.Form):
    supplement_type = forms.ChoiceField(choices=SUPPLEMENT_TYPE_CHOICES)
    uploaded_file = forms.ImageField()

    def error_message(self):
        if self.errors['uploaded_file']:
            return (u'มีข้อผิดพลาดเกี่ยวกับแฟ้มที่อัพโหลด: ' +  
                    u','.join([u'%s' % e for e in self.errors['uploaded_file']]))
        else:
            return 'ข้อมูลในฟอร์มผิดพลาด'

def allowed_applicant_required(view_function):
    @submitted_applicant_required
    def decorate(request, *args, **kwargs):
        if request.applicant.submission_info.doc_reviewed_complete:
            return render_to_response('supplement/already_complete.html',
                                      { 'applicant': request.applicant })
        else:
            return view_function(request, *args, **kwargs)

    return decorate

def within_deadline_required(view_function):
    def decorate(request, *args, **kwargs):
        if supplement_submission_deadline_passed():
            return HttpResponseRedirect(reverse('commons-deadline-error'))
        else:
            return view_function(request, *args, **kwargs)

    return decorate

    

# this is for showing step bar
SUPPLEMENTS_FORM_STEPS = [
    ('ส่งหลักฐานเพิ่มเติมแบบออนไลน์','supplement-index'),
    ('กลับไปหน้าแสดงสถานะการสมัคร','status-index'),
    ]

@within_deadline_required
@allowed_applicant_required
def index(request):
    applicant = request.applicant
    supplements = applicant.supplements
    form = SupplementForm()

    error = extract_variable_from_session_or_none(request.session, 'error')

    form_step_info = { 'steps': SUPPLEMENTS_FORM_STEPS,
                       'current_step': 0,
                       'max_linked_step': 1 }

    return render_to_response('supplement/index.html',
                              { 'applicant': applicant,
                                'supplements': supplements,
                                'form': form,
                                'form_step_info': form_step_info,
                                'upload_error': error,
                                'can_log_out': True })

def upload_error(request, error):
    request.session['error'] = error
    return HttpResponseRedirect(reverse('supplement-index'))

@within_deadline_required
@allowed_applicant_required
def supp_get_img(request, supplement_id):
    supplement = get_object_or_404(Supplement, pk=supplement_id)
    if supplement.applicant_id != request.applicant.id:
        return HttpResponseNotFound()
    
    filename = supplement.preview_path()
    if not os.path.exists(filename):
        supplement.create_preview()

    if os.path.exists(filename):
        return serve_file(filename)
    else:
        return HttpResponseNotFound()

@within_deadline_required
@allowed_applicant_required
def delete_supplement(request, supplement_id):
    supplement = get_object_or_404(Supplement, pk=supplement_id)
    if supplement.applicant_id != request.applicant.id:
        return HttpResponseNotFound()

    supplement.delete()
    return HttpResponseRedirect(reverse('supplement-index'))

@allowed_applicant_required
def upload(request):
    if request.method!='POST':
        return HttpResponseForbidden()

    try:
        if request.applicant.supplements.count() >= settings.MAX_SUPPLEMENTS:
            return upload_error(request, 'คุณได้อัพโหลดหลักฐานเป็นจำนวนมากเกินไป')
    except:
        pass

    form = SupplementForm(request.POST, request.FILES)

    if supplement_submission_deadline_passed():
        return HttpResponseRedirect(reverse('commons-deadline-error'))        

    if form.is_valid():
        f = request.FILES['uploaded_file']

        if f.size > settings.MAX_UPLOADED_DOC_FILE_SIZE:
            return upload_error(request, 'แฟ้มที่ส่งมามีขนาดใหญ่เกินไป')

        supplement = Supplement()
        supplement.applicant = request.applicant
        supplement.supplement_type = SUPPLEMENTS[int(form.cleaned_data['supplement_type'])]
        supplement.image = f
        supplement.save()

        submission_info = request.applicant.submission_info
        submission_info.update_last_updated_timestamp_to_now()

        return HttpResponseRedirect(reverse('supplement-index'))

    return upload_error(request, form.error_message())
