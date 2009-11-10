# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from commons.decorators import applicant_required

from application.models import Applicant
from application.views import redirect_to_applicant_first_page

def submitted_applicant_required(view_function):
    """
    returns a view function that checks if the applicant has submitted
    the application, otherwise redirect to the applicant first page.
    """
    @applicant_required
    def decorate(request, *args, **kwargs):
        if request.applicant.is_submitted:
            return view_function(request, *args, **kwargs)
        else:
            return redirect_to_applicant_first_page(request.applicant)

    return decorate


@submitted_applicant_required
def index(request):
    return render_to_response("application/status/index.html",
                              { 'applicant': request.applicant })


# this is for showing step bar
SHOW_UPLOAD_FORM_STEPS_ONLINE = [
    ('ดูข้อมูลที่ใช้สมัคร','status-show'),
    ('ดูหลักฐานที่อัพโหลดแล้ว','upload-show'),
    ]

SHOW_UPLOAD_FORM_STEPS_POSTAL = [
    ('ดูข้อมูลที่ใช้สมัคร','status-show'),
    ('ดูและพิมพ์ใบนำส่ง','status-show-ticket'),
    ]

@submitted_applicant_required
def show(request):
    if request.applicant.online_doc_submission():
        form_step_info = { 'steps': SHOW_UPLOAD_FORM_STEPS_ONLINE,
                           'current_step': 0,
                           'max_linked_step': 1 }
    else:
        form_step_info = { 'steps': SHOW_UPLOAD_FORM_STEPS_POSTAL,
                           'current_step': 0,
                           'max_linked_step': 1 }
    return render_to_response("application/status/show.html",
                              { 'applicant': request.applicant,
                                'form_step_info': form_step_info })


@submitted_applicant_required
def show_ticket(request):
    if request.applicant.online_doc_submission():
        # on-line submission does have ticket
        return HttpResponseRedirect(reverse('status-show'))
    else:
        form_step_info = { 'steps': SHOW_UPLOAD_FORM_STEPS_POSTAL,
                           'current_step': 1,
                           'max_linked_step': 1 }
    return render_to_response("application/status/show_ticket.html",
                              { 'applicant': request.applicant,
                                'form_step_info': form_step_info })

