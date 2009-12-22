# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from commons.decorators import applicant_required
from commons.decorators import submitted_applicant_required
from commons.utils import submission_deadline_passed, supplement_submission_deadline_passed

from commons.email import send_status_by_email_no_applicant
from commons.email import send_status_by_email_not_submitted
from commons.email import send_status_by_email_many_submitted_apps
from commons.email import send_status_by_email

from application.models import Applicant
from application.views import redirect_to_applicant_first_page
from application.forms import StatusRequestForm

from review.models import ReviewFieldResult

@submitted_applicant_required
def index(request):
    notice = ''
    if 'notice' in request.session:
        notice = request.session['notice']
        del request.session['notice']

    submission_info = request.applicant.submission_info
    if submission_info.has_been_reviewed:
        review_results = ReviewFieldResult.get_applicant_review_error_results(request.applicant)
    else:
        review_results = None

    return render_to_response("application/status/index.html",
                              { 'applicant': request.applicant,
                                'submission_info': submission_info,
                                'review_results': review_results,
                                'submission_deadline_passed':
                                    submission_deadline_passed(),
                                'supplement_submission_deadline_passed':
                                    supplement_submission_deadline_passed(),
                                'notice': notice,
                                'can_log_out': True })


# this is for showing step bar
SHOW_UPLOAD_FORM_STEPS_ONLINE = [
    ('ดูข้อมูลที่ใช้สมัคร','status-show'),
    ('ดูหลักฐานที่อัพโหลดแล้ว','upload-show'),
    ('กลับไปหน้าสถานะใบสมัคร','status-index'),
    ]

SHOW_UPLOAD_FORM_STEPS_POSTAL = [
    ('ดูข้อมูลที่ใช้สมัคร','status-show'),
    ('ดูและพิมพ์ใบนำส่ง','status-show-ticket'),
    ('กลับไปหน้าสถานะใบสมัคร','status-index'),
    ]

@submitted_applicant_required
def show(request):
    if request.applicant.online_doc_submission():
        form_step_info = { 'steps': SHOW_UPLOAD_FORM_STEPS_ONLINE,
                           'current_step': 0,
                           'max_linked_step': 2 }
    else:
        form_step_info = { 'steps': SHOW_UPLOAD_FORM_STEPS_POSTAL,
                           'current_step': 0,
                           'max_linked_step': 2 }
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
                           'max_linked_step': 2 }
    return render_to_response("application/status/show_ticket.html",
                              { 'applicant': request.applicant,
                                'form_step_info': form_step_info })


def request_status(request):
    notice = ''
    if request.method == 'POST':
        form = StatusRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            applicants = Applicant.objects.filter(email__endswith=email).all()
            real_applicants = [a for a in applicants if a.get_email() == email]
            if len(real_applicants)==0:
                send_status_by_email_no_applicant(email)
            else:
                submitted_applicants = [a for a in real_applicants if a.is_submitted] 
                if len(submitted_applicants)==1:
                    send_status_by_email(submitted_applicants[0])
                elif len(submitted_applicants)==0:
                    send_status_by_email_not_submitted(email, real_applicants)
                else:
                    send_status_by_email_many_submitted_apps(submitted_applicants)
            notice = u'ระบบได้จัดส่งจดหมายอิเล็กทรอนิกส์ไปยัง ' + email + u' แล้ว'
    else:
        form = StatusRequestForm()

    return render_to_response('application/status/request.html', 
                              { 'form': form,
                                'notice': notice })
    
