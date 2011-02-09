# -*- coding: utf-8 -*-
from random import randint
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings

from commons.decorators import applicant_required
from commons.decorators import submitted_applicant_required
from commons.utils import submission_deadline_passed, supplement_submission_deadline_passed, admission_major_pref_deadline_passed, round2_confirmation_deadline_passed

from commons.email import send_status_by_email_no_applicant
from commons.email import send_status_by_email_not_submitted
from commons.email import send_status_by_email_many_submitted_apps
from commons.email import send_status_by_email
from commons.email import send_admission_status_by_mail
from commons.email import send_final_admission_status_by_mail
from commons.email import send_admission_status_problem_by_mail

from application.models import Applicant, GPExamDate
from application.views import redirect_to_applicant_first_page
from application.forms import StatusRequestForm

from review.models import ReviewFieldResult
from result.models import AdmissionResult, AdmissionRound
from confirmation.models import Round2ApplicantConfirmation, AdmissionMajorPreference

def prepare_exam_scores(applicant):
    try:
        niets_scores = applicant.NIETS_scores
    except:
        niets_scores = None
    if not niets_scores:
        return None

    cal_scores = niets_scores.as_calculated_list_by_exam_round()
    scores = []

    test_names = ['gat','pat1','pat3']
    test_norm_scores = dict([(n,[]) for n in test_names])

    for i in range(len(cal_scores)):
        scores.append({'date': GPExamDate.get_by_id(i+1),
                       'scores': cal_scores[i]})
        for n in test_names:
            test_norm_scores[n].append(cal_scores[i][n]['normalized'])

    best_scores = dict([(n,max(test_norm_scores[n])) for n in test_names])
    final_score = niets_scores.get_score()

    return { 'scores': scores, 
             'best_scores': best_scores,
             'final_score': final_score }
        

def copy_previous_adm_major_pref(prev_pref,
                                 applicant,
                                 admitted_major,
                                 round_number):
    new_pref = AdmissionMajorPreference.new_for_applicant(applicant, 
                                                          prev_pref.is_accepted_list)
    new_pref.round_number = round_number
    new_pref.set_ptype_cache(save=False)
    return new_pref


@submitted_applicant_required
def index(request):
    notice = ''
    if 'notice' in request.session:
        notice = request.session['notice']
        del request.session['notice']

    submission_info = request.applicant.submission_info
    random_seed = 1000000 + randint(0,8999999)

    applicant = request.applicant

    admission_result = None
    admission_major_pref = None
    admitted_major = None
    latest_admission_major_pref = None
    latest_admission_result = None
    is_adm_major_pref_copied_from_prev_round = False
    student_registration = None

    accepting_majors = None

    first_admission = False

    current_round = AdmissionRound.get_recent()

    is_last_round = True

    if current_round:
        admission_result = applicant.get_latest_admission_result()

        first_admission = (applicant.admission_results.count() == 1)

        admission_major_pref = applicant.get_admission_major_preference(current_round.number)

        if not admission_major_pref:
            all_major_prefs = list(applicant.admission_major_preferences.all())
            if len(all_major_prefs)>0:
                latest_admission_major_pref = all_major_prefs[0]

                if admission_result:
                    # accepted, copy previous pref
                    admission_major_pref = copy_previous_adm_major_pref(
                        latest_admission_major_pref, 
                        applicant,
                        admitted_major,
                        current_round.number)
                    admission_major_pref.save()

        if admission_major_pref:
            accepting_majors = admission_major_pref.get_accepted_majors(check_admitted=False)
        elif latest_admission_major_pref:
            # for those who picked choice 3
            accepting_majors = latest_admission_major_pref.get_accepted_majors(check_admitted=False)
            

        if admission_result:
            admitted_major = admission_result.admitted_major
            student_registration = applicant.get_student_registration()

        if not admission_result:
            results = applicant.admission_results.filter(round_number__lte=current_round.number).all()
            if len(results)>0:
                latest_admission_result = results[len(results)-1]

    confirmations = applicant.admission_confirmations.all()
    total_amount_confirmed = sum([c.paid_amount for c in confirmations])

    if admitted_major and (total_amount_confirmed >= admitted_major.confirmation_amount):
        confirmation_complete = True
        additional_payment = 0
    else:
        confirmation_complete = False
        if admitted_major:
            additional_payment = admitted_major.confirmation_amount - total_amount_confirmed
        else:
            additional_payment = 0

    if len(confirmations)!=0:
        recent_confirmation = confirmations[0]
    else:
        recent_confirmation = None

    is_confirmation_time_left = (AdmissionRound.time_to_recent_round_deadline() > timedelta(0))

    return render_to_response("application/status/index.html",
                              { 'applicant': request.applicant,
                                'submission_info': submission_info,
                                'admission_result': admission_result,
                                'first_admission': first_admission,
                                'latest_admission_result':
                                    latest_admission_result,
                                'admission_major_pref': admission_major_pref,
                                'accepting_majors': accepting_majors,
                                'latest_admission_major_pref':
                                    latest_admission_major_pref,
                                'is_adm_major_pref_copied_from_prev_round':
                                    is_adm_major_pref_copied_from_prev_round,

                                'confirmation_complete': confirmation_complete,
                                'recent_confirmation': recent_confirmation,
                                'confirmations': confirmations,
                                'total_amount_confirmed': total_amount_confirmed,
                                'additional_payment': additional_payment,

                                'student_registration':
                                    student_registration,

                                'current_round': current_round,
                                'is_last_round': is_last_round,
                                'is_confirmation_time_left': is_confirmation_time_left,
                                'random_seed': random_seed,
                                'notice': notice,
                                'can_log_out': True })


@submitted_applicant_required
def show_score(request):
    notice = ''
    if 'notice' in request.session:
        notice = request.session['notice']
        del request.session['notice']

    exam_scores = prepare_exam_scores(request.applicant)

    return render_to_response("application/status/score.html",
                              { 'applicant': request.applicant,
                                'exam_scores': exam_scores,
                                'notice': notice,
                                'can_log_out': True })


# this is for showing step bar
SHOW_UPLOAD_FORM_STEPS_ONLINE = [
    ('ดูข้อมูลที่ใช้สมัคร','status-show'),
    ('กลับไปหน้าสถานะใบสมัคร','status-index'),
    ]

SHOW_UPLOAD_FORM_STEPS_POSTAL = [
    ('ดูข้อมูลที่ใช้สมัคร','status-show'),
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


def filter_admitted_applicants(applicants):
    if len(applicants)==1:
        return applicants[0]

    apps_with_nat_id = [a for a in applicants
                         if a.has_personal_info()]
    nat_id_set = set([a.personal_info.national_id 
                      for a in apps_with_nat_id])

    if len(nat_id_set)!=1:
        return None
    else:
        return apps_with_nat_id[0]

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


AMOUNT_STRINGS = {0: u'ศูนย์บาทถ้วน',
                  16000: u'หนึ่งหมื่นหกพันบาทถ้วน',
                  20700: u'สองหมื่นเจ็ดร้อยบาทถ้วน',
                  24000: u'สองหมื่นสี่พันบาทถ้วน',
                  36700: u'สามหมื่นหกพันเจ็ดร้อยบาทถ้วน',
                  44700: u'สี่หมื่นสี่พันเจ็ดร้อยบาทถ้วน',
                  60700: u'หกหมื่นเจ็ดร้อยบาทถ้วน'}

@submitted_applicant_required
def confirmation_ticket(request):
    applicant = request.applicant
    admitted = applicant.is_admitted()

    if not admitted:
        raise Http404

    if not request.applicant.is_submitted:
        return render_to_response('application/submission/ticket_not_submitted.html')

    current_round = AdmissionRound.get_recent()
    round_number = current_round.number
    admission_result = applicant.get_latest_admission_result()
    admission_pref = applicant.get_admission_major_preference(round_number)

    if not admission_pref:
        raise Http404

    confirmations = applicant.admission_confirmations.all()
    total_amount_confirmed = sum([c.paid_amount for c in confirmations])

    amount = admission_result.admitted_major.confirmation_amount - total_amount_confirmed
    if amount < 0:
        amount = 0

    if amount in AMOUNT_STRINGS:
        amount_str = AMOUNT_STRINGS[amount]
    else:
        amount_str = str(amount)

    deadline = current_round.last_date
    msg = u'ยืนยันสิทธิ์การเข้าศึกษาต่อในสาขา' + admission_result.admitted_major.name

    verification = request.applicant.verification_number(settings.CONFIRMATION_HASH_MAGIC)
    return render_to_response('application/payin/ticket.html',
                              {'amount': amount,
                               'amount_str': amount_str,
                               'applicant': request.applicant,
                               'verification': verification,
                               'deadline': deadline,
                               'msg': msg })
        
    

def request_status(request):
    notice = ''
    if request.method == 'POST':
        form = StatusRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            applicants = Applicant.objects.filter(email__iendswith=email).all()
            real_applicants = [a for a in applicants 
                               if a.get_email().lower() == email.lower()]
            if len(real_applicants)==0:

                send_status_by_email_no_applicant(email)
                notice = u'ระบบได้จัดส่งจดหมายอิเล็กทรอนิกส์ไปยัง ' + email + u' แล้ว'
            else:
                if (settings.SHOW_FINAL_ADMISSION_RESULTS) or (settings.SHOW_ADMISSION_RESULTS):
                    applicant = filter_admitted_applicants(real_applicants)
                    if applicant!=None:
                        if settings.SHOW_FINAL_ADMISSION_RESULTS:
                            send_final_admission_status_by_mail(applicant)
                        else:
                            send_admission_status_by_mail(applicant)
                        notice = u'ระบบได้จัดส่งจดหมายอิเล็กทรอนิกส์ไปยัง ' + email + u' แล้ว'
                    else:
                        send_admission_status_problem_by_mail(email)
                        notice = u'มีปัญหาในการเรียกค้น ระบบได้จัดส่งจดหมายอิเล็กทรอนิกส์ไปยัง ' + email + u' แล้ว'
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
    
