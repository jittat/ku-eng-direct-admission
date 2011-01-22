# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from commons.decorators import submitted_applicant_required
from commons.utils import admission_major_pref_deadline_passed, round2_confirmation_deadline_passed
from commons.models import Log
from application.models import Applicant, SubmissionInfo, Major, Education, PersonalInfo
from result.models import NIETSScores, AdmissionResult, AdmissionRound

from models import AdmissionMajorPreference, AdmissionConfirmation, Round2ApplicantConfirmation

from django import forms
from django.forms import ModelForm

def get_higher_ranked_majors(majors, current_major):
    result = []
    for m in majors:
        if m.id != current_major.id:
            result.append(m)
        else:
            return result
        

def check_form_submission(post_data, higher_majors):
    if (('pref_type' not in post_data) or
        (post_data['pref_type'] not in ['no_move',
                                        'move_up_inclusive',
                                        'move_up_strict',
                                        'withdrawn'])):
        return False, 'เลือกประเภทการพิจารณาไม่ถูกต้อง, กรุณาเลือก 1 ข้อ'
    if post_data['pref_type'] in ['move_up_strict', 'move_up_inclusive']:
        mcount = len(higher_majors)
        for i in range(mcount):
            if ('major-accepted-' + str(i+1)) in post_data:
                return True, ''
        return False, 'กรุณาเลือกสาขาที่ต้องการให้พิจารณาเลื่อนอันดับอย่างน้อย 1 สาขา'
    return True, ''

def update_admission_major_preference(pref, applicant,
                                      preferred_majors,
                                      higher_majors,
                                      round_number,
                                      post_data):
    if not pref:
        pref = AdmissionMajorPreference()

    pref.applicant = applicant
    pref.round_number = round_number
    
    alist = [0] * len(preferred_majors)
    if post_data['pref_type'] in ['move_up_inclusive', 'move_up_strict']:
        for i in range(len(higher_majors)):
            if ('major-accepted-' + str(i+1)) in post_data:
                alist[i] = 1
    if post_data['pref_type'] in ['no_move', 'move_up_inclusive']:
        alist[len(higher_majors)] = 1    # current admitted major

    pref.is_accepted_list = alist
    return pref

@submitted_applicant_required
def pref(request):
    applicant = request.applicant
    admitted = applicant.is_admitted()

    if not admitted:
        raise Http404

    # check for deadline
    if admission_major_pref_deadline_passed():
        return render_to_response('confirmation/pref_deadline_passed.html')

    current_round = AdmissionRound.get_recent()
    round_number = current_round.number
    admission_result = applicant.get_latest_admission_result()

    preferred_majors = applicant.preference.get_major_list()
    higher_majors = get_higher_ranked_majors(preferred_majors, 
                                             admission_result.admitted_major)

    
    admission_pref = applicant.get_admission_major_preference(round_number)

    if admission_pref:
        pref_type = admission_pref.get_pref_type()
        accepted_major_ids = [m.id for m in admission_pref.get_accepted_majors()]
        is_accepted_list = [(m.id in accepted_major_ids)
                            for m in higher_majors]
    else:
        pref_type = AdmissionMajorPreference.PrefType.new_empty()
        try:
            is_accepted_list = [False] * len(higher_majors)
        except:
            Log.create("Error: empty higher majors: %d" % (applicant.id,))
            raise

    form_check_message = ''

    if request.method=='POST':
        if 'submit' in request.POST:
            check_result, form_check_message = check_form_submission(request.POST, higher_majors)
            if check_result:
                admission_pref = update_admission_major_preference(
                    admission_pref,
                    applicant, preferred_majors,
                    higher_majors, 
                    round_number,
                    request.POST)
                admission_pref.set_ptype_cache(save=False)
                admission_pref.save()
                request.session['notice'] = 'เก็บข้อมูลการยืนยันอันดับการเลือกสาขาวิชาแล้ว'

                Log.create("confirmation - from: %s,type: %d (%s), val: %s" %
                           (request.META['REMOTE_ADDR'],
                            admission_pref.get_pref_type().ptype,
                            request.POST['pref_type'],
                            str(admission_pref.is_accepted_list)),
                           applicant_id=applicant.id,
                           applicantion_id=applicant.submission_info.applicantion_id)

                return HttpResponseRedirect(reverse('status-index'))
        else:
            if admission_pref:
                request.session['notice'] = 'ยกเลิกการแก้ไขอันดับการเลือกสาขาวิชา'
            else:
                request.session['notice'] = 'ยกเลิกการยืนยันอันดับการเลือกสาขาวิชา'

            Log.create("confirmation: cancel",
                       applicant_id=applicant.id,
                       applicantion_id=applicant.submission_info.applicantion_id)

            return HttpResponseRedirect(reverse('status-index'))
    else:
        pass

    return render_to_response('confirmation/pref.html',
                              { 'applicant': applicant,
                                'admission_result': admission_result,
                                'current_round': current_round,
                                'higher_majors': higher_majors,
                                'majors_with_is_accepted':
                                    zip(higher_majors, is_accepted_list),
                                'admission_pref': admission_pref,
                                'pref_type': pref_type,
                                'form_check_message': form_check_message })

def get_best_scores(applicant):
    try:
        niets_scores = applicant.NIETS_scores
    except:
        return None

    return niets_scores.get_best_test_scores()

def render_confirmed_applicant(applicant):
    admission_result = applicant.admission_result
    preferred_majors = applicant.preference.get_major_list()
    higher_majors = get_higher_ranked_majors(preferred_majors, 
                                             admission_result.admitted_major)
    best_scores = get_best_scores(applicant)

    admission_pref = applicant.admission_major_preference
    pref_type = admission_pref.get_pref_type()
    accepted_major_ids = [m.id for m in admission_pref.get_accepted_majors()]
    is_accepted_list = [(m.id in accepted_major_ids)
                        for m in higher_majors]
     
    return render_to_response('confirmation/show_confirmed.html',
                              { 'applicant': applicant,
                                'best_scores': best_scores,
                                'admission_result': admission_result,
                                'higher_majors': higher_majors,
                                'majors_with_is_accepted':
                                    zip(higher_majors, is_accepted_list),
                                'admission_pref': admission_pref,
                                'pref_type': pref_type })


def render_unconfirmed_applicant(applicant):
    admission_result = applicant.admission_result
    preferred_majors = applicant.preference.get_major_list()
    higher_majors = get_higher_ranked_majors(preferred_majors, 
                                             admission_result.admitted_major)
    best_scores = get_best_scores(applicant)
    return render_to_response('confirmation/show_unconfirmed.html',
                              { 'applicant': applicant,
                                'best_scores': best_scores,
                                'admission_result': admission_result,
                                'higher_majors': higher_majors })

@login_required
def interview_info(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    try:
        pref = applicant.admission_major_preference
    except:
        pref = None

    if pref:
        return render_confirmed_applicant(applicant)
    else:
        return render_unconfirmed_applicant(applicant)

def build_pref_stat(adm_round):
    results = (AdmissionResult.
               objects.
               filter(round_number=adm_round.number).
               all())
    app_results = dict([(r.applicant_id,r) for r in results])
    
    adm_major_prefs = AdmissionMajorPreference.objects.filter(round_number=adm_round.number).all()

    majors = Major.objects.all()

    major_number_dict = dict([(m.id,int(m.number)) for m in majors])

    pref_tab = {} #dict([(int(m.number),[]) for m in majors])
    for m in majors:
        pref_tab[int(m.number)] = []
        for i in range(4):
            pref_tab[int(m.number)].append([0,0])

    confirmed_app = set([c.applicant_id 
                         for c in
                         AdmissionConfirmation.objects.filter(round_number=adm_round.number).all()])


    for p in adm_major_prefs:
        app_id = p.applicant_id
        t = p.get_pref_type().ptype
        if app_id in app_results:
            major_number = major_number_dict[app_results[app_id].admitted_major_id]
            pref_tab[major_number][t-1][0] += 1
            if app_id in confirmed_app:
                pref_tab[major_number][t-1][1] += 1

    pref_stat = []
    for m in majors:
        pref_stat.append({'major': m,
                          'pref_counts': pref_tab[int(m.number)]})
    return pref_stat



@login_required
def index(request):
    adm_round = AdmissionRound.get_recent()

    pref_stat = build_pref_stat(adm_round)

    if 'notice' in request.session:
        notice = request.session['notice']
        del request.session['notice']
    else:
        notice = ''

    return render_to_response('confirmation/index.html',
                              { 'pref_stat': pref_stat,
                                'admission_round': adm_round,
                                'notice': notice })


@login_required
def list_confirmed_applicants(request, major_number):
    major = Major.objects.get(number=major_number)
    adm_round = AdmissionRound.get_recent()

    results = (AdmissionResult.
               objects.
               filter(round_number=adm_round.number).
               filter(admitted_major=major).
               select_related(depth=1).
               all())

    applicants = [r.applicant for r in results]
    app_dict = dict([(r.applicant_id,r.applicant) for r in results])

    adm_major_pref = (AdmissionMajorPreference.
                      objects.
                      filter(round_number=adm_round.number).
                      filter(applicant__in=applicants))

    # confirmation statistics
    confirmations = (AdmissionConfirmation.
                     objects.
                     filter(applicant__in=applicants))

    for a in applicants:
        a.confirmed_amount = 0
    for c in confirmations:
        if c.applicant_id in app_dict:
            app_dict[c.applicant_id].confirmed_amount += c.paid_amount

    for a in applicants:
        a.has_confirmed = (a.confirmed_amount >= major.confirmation_amount)

    confirmed_applicants = [[],[],[],[]]
    for p in adm_major_pref:
        t = p.get_pref_type().ptype - 1
        confirmed_applicants[t].append(app_dict[p.applicant_id])

    for t in range(4):
        confirmed_applicants[t] = sorted(confirmed_applicants[t],
                                         cmp=lambda x,y: cmp(-x.confirmed_amount, -y.confirmed_amount))
        

    titles = [u'ไม่ขอเลื่อนอันดับ',
              u'ยืนยันสิทธิ์ ขอพิจารณาเลื่อนอันดับ ถ้าไม่ได้เลื่อนขอรักษาสิทธิ์',
              u'ยืนยันสิทธิ์ ขอพิจารณาเลื่อนอันดับ ถ้าไม่ได้เลื่อนขอสละสิทธิ์',
              u'สละสิทธิ์']

    return render_to_response('confirmation/list_applicants.html',
                              { 'admisison_round': adm_round,
                                'major': major,
                                'confirmed_apps_groups':
                                    zip(titles, confirmed_applicants),
                                'results': results })
    


##############################################


def get_confirming_apps_with_majors():
    majors = Major.get_all_majors()
    confirmations = AdmissionConfirmation.objects.select_related(depth=1).all() 
    results = AdmissionResult.objects.filter(
        applicant__in=[c.applicant for c in confirmations])
    res_dict = dict([(r.applicant_id,r) for r in results])

    apps = dict([(m.id, []) for m in majors])
    for con in confirmations:
        app = con.applicant
        admission_result = res_dict[app.id]
        app.admission_result = admission_result
        if admission_result.is_final_admitted:
            major_id = admission_result.final_admitted_major_id
            apps[major_id].append(app)

    stat = []
    for major in majors:
        stat.append((major, apps[major.id]))
    return stat

def get_all_confirming_apps():
    confirmations = AdmissionConfirmation.objects.select_related(depth=1).all() 
    results = AdmissionResult.objects.filter(
        applicant__in=[c.applicant for c in confirmations])
    res_dict = dict([(r.applicant_id,r) for r in results])

    apps = []
    for con in confirmations:
        app = con.applicant
        admission_result = res_dict[app.id]
        app.admission_result = admission_result
        apps.append(app)

    return apps

def cache_apps_score(apps):
    educations = Education.objects.filter(applicant__in=apps)
    gpaxdict = dict([(e.applicant_id,e.gpax) 
                     for e in educations])
    scores = NIETSScores.objects.filter(applicant__in=apps)
    sdict = dict([(s.applicant_id, s.get_score(gpaxdict[s.applicant_id]))
                  for s in scores])
    for a in apps:
        try:
            a.score = sdict[a.id]
        except:
            # for A-NET apps
            a.score = None

def cache_apps_fields(apps, models, field_names):
    for a in apps:
        try:
            if a.field_cache == None:
                a.field_cache = {}
        except:
            a.field_cache = {}

    for model, name in zip(models,field_names):
        results = model.objects.filter(applicant__in=apps)
        d = dict([(r.applicant_id, r) for r in results])
        for a in apps:
            a.field_cache[name] = d[a.id]

def get_confirmation_stat_with_majors():
    score_stat = {}
    confirming_apps = get_confirming_apps_with_majors()
    for m, apps in confirming_apps:
        cache_apps_score(apps)
        ma = apps[0].score
        mi = ma
        for a in apps:
            s = a.score
            if s!=None:
                if s<mi:
                    mi = s
                if s>ma:
                    ma = s
        score_stat[m.id] = (mi,ma)

    return [(s[0],len(s[1]),score_stat[s[0].id]) 
            for s in confirming_apps]

@login_required
def confirmation_stat(request):
    confirmation_stat = get_confirmation_stat_with_majors()

    return render_to_response('confirmation/stat.html',
                              { 'confirmation_stat': confirmation_stat })

def write_csv_output(major_apps):
    import csv
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=assignment.csv'

    content = []

    content.append(','.join(['Application_ID', 
                             'Title',
                             'FirstName', 
                             'LastName', 
                             'Score', 
                             'Major',
                             'MajorName',]))
    for m,apps in major_apps:
        cache_apps_score(apps)
        cache_apps_fields(apps,
                          [PersonalInfo, SubmissionInfo],
                          ['pinfo', 'subinfo'])
        for a in apps:
            score = a.score
            if score==None:
                score = a.education.anet
            a.submission_info = a.field_cache['subinfo']
            if a.admission_result.is_admitted:
                major_name = a.admission_result.admitted_major.number
            else:
                major_name = ''
            content.append(u','.join(
                    [a.ticket_number(),
                     a.title,
                     a.first_name,
                     a.last_name,
                     str(score),
                     str(m.number),
                     m.name]
                    ))
    content.append('')
    response.content = '\n'.join(content)
    return response

def write_csv_output_for_registra(major_apps):
    import csv
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=assignment_registra.csv'

    content = []

    content.append(u','.join([u'ลำดับ',
                              u'เลขประจำตัวสอบ',
                              u'เลขบัตรประชาชน',
                              u'คำนำหน้า',
                              u'ชื่อ', 
                              u'นามสกุล', 
                              u'โรงเรียนที่จบ', 
                              u'สาขาวิชา',
                              u'คณะ',
                              u'มหาวิทยาลัย']))
    count = 0
    for m,apps in major_apps:
        cache_apps_score(apps)
        cache_apps_fields(apps,
                          [PersonalInfo, SubmissionInfo, Education],
                          ['pinfo', 'subinfo', 'edu'])
        for a in apps:
            score = a.score
            if score==None:
                score = a.education.anet
            a.submission_info = a.field_cache['subinfo']
            content.append(u','.join(
                    [str(count + 1),
                     a.ticket_number(),
                     a.field_cache['pinfo'].national_id,
                     a.title,
                     a.first_name,
                     a.last_name,
                     a.field_cache['edu'].school_name,
                     m.name,
                     u'วิศวกรรมศาสตร์',
                     u'มก.']
                    ))
            count += 1
    content.append(u'')
    response.content = u'\n'.join(content)
    return response

def write_payment_csv_output(applicants):
    import csv
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=assignment.csv'

    content = []

    content.append(','.join(['Application_ID', 
                             'National_ID',
                             'Title',
                             'FirstName', 
                             'LastName',
                             'Score',
                             'FirstRound',
                             'FirstMajor',
                             'Amount',
                             'FinalRound',
                             'FinalMajor',
                             'Amount',
                             ]))
    cache_apps_score(applicants)
    cache_apps_fields(applicants,
                      [PersonalInfo, SubmissionInfo],
                      ['pinfo', 'subinfo'])

    payments = [0] + [16000]*7 + [36700]*3 + [60700]*3

    for a in applicants:
        score = a.score
        if score==None:
            score = a.education.anet
        a.submission_info = a.field_cache['subinfo']
        if a.admission_result.is_admitted:
            first_major = a.admission_result.admitted_major_id
            first_amount = payments[first_major]
        else:
            first_major = 0
            first_amount = 0
        if a.admission_result.is_final_admitted:
            final_major = a.admission_result.final_admitted_major_id
            final_amount = payments[final_major]
        else:
            final_major = 0
            final_amount = 0
        content.append(u','.join(
                [a.ticket_number(),
                 a.field_cache['pinfo'].national_id,
                 a.title,
                 a.first_name,
                 a.last_name,
                 str(score),
                 str(a.admission_result.is_admitted),
                 str(first_major),
                 str(first_amount),
                 str(a.admission_result.is_final_admitted),
                 str(final_major),
                 str(final_amount),
                 ]
                ))
        
    content.append('')
    response.content = '\n'.join(content)
    return response

@login_required
def confirmation_stat_download(request):
    return write_csv_output(get_confirming_apps_with_majors())

@login_required
def confirmation_stat_download_for_registra(request):
    return write_csv_output_for_registra(get_confirming_apps_with_majors())

@login_required
def confirmation_payment_net_download(request):
    return write_payment_csv_output(get_all_confirming_apps())

@login_required
def confirm(request, preview=False):
    """
    Obsoleted.
    """

    return HttpResponseForbidden()

    if request.method != 'POST':
        return HttpResponseForbidden()
    if not request.user.has_perm('confirmation.add_admissionconfirmation'):
        return HttpResponseForbidden('ขออภัยคุณไม่มีสิทธิ์ในการทำรายการดังกล่าว')

    if 'cancel' in request.POST:
        request.session['notice'] = u'ยกเลิกการทำรายการ'
        return HttpResponseRedirect(reverse('confirmation-index'))

    import re

    if (('application_id' not in request.POST) or
        (not re.match(r'53[123]\d{5}', request.POST['application_id']))):
        request.session['notice'] = u'เกิดข้อผิดพลาด หมายเลขประจำตัวผู้สมัครไม่ถูกต้อง'
        return HttpResponseRedirect(reverse('confirmation-index'))

    application_id = request.POST['application_id']
    submission_info = SubmissionInfo.find_by_ticket_number(application_id)
    if submission_info==None:
        request.session['notice'] = (u'เกิดข้อผิดพลาด ไม่พบผู้สมัครที่ใช้หมายเลข %s' % application_id)
        return HttpResponseRedirect(reverse('confirmation-index'))

    applicant = submission_info.applicant

    if (not applicant.has_admission_result() or
        not applicant.admission_result.is_final_admitted):
        request.session['notice'] = (u'เกิดข้อผิดพลาด ผู้สมัครที่ใช้หมายเลข %s (%s) '
                                     u'ไม่ผ่านการคัดเลือกเข้าศึกษาต่อ' % 
                                     (application_id, applicant.full_name()))
        return HttpResponseRedirect(reverse('confirmation-index'))


    try:
        if applicant.admission_confirmation!=None:
            request.session['notice'] = (u'เกิดข้อผิดพลาด ผู้สมัครที่ใช้หมายเลข %s (%s) '
                                         u'ได้ยืนยันสิทธิ์แล้ว ถ้าต้องการยกเลิกกรุณาแจ้งผู้ดูแล' % 
                                         (application_id, applicant.full_name()))
            return HttpResponseRedirect(reverse('confirmation-index'))            
    except:
        pass

    if preview:
        return render_to_response('confirmation/preview.html',
                                  { 'applicant': applicant })
    else:
        confirmation = AdmissionConfirmation(applicant=applicant,
                                             confirming_user=request.user)

        Log.create("admission confirmation - from: %s" %
                   (request.META['REMOTE_ADDR'],),
                   user=request.user.username,
                   applicant_id=applicant.id,
                   applicantion_id=application_id)

        try:
            confirmation.save()
        except:
            Log.create("ERROR: admission confirmation - from: %s" %
                       (request.META['REMOTE_ADDR'],),
                       user=request.user.username,
                       applicant_id=applicant.id,
                       applicantion_id=application_id)

            request.session['notice'] = u'เกิดข้อผิดพลาดในการยืนยันสิทธิ์ กรุณาแจ้งผู้ดูแลด่วน'
            return HttpResponseRedirect(reverse('confirmation-index'))            

        request.session['notice'] = u'บันทึกการยืนยันสิทธิ์เรียบร้อย ชื่อผู้ยืนยันควรปรากฏในตารางด้านล่าง'
        return HttpResponseRedirect(reverse('confirmation-index'))            


def render_confirmation_form_second_round(request, applicant):
    second_round_admitted = False
    if applicant.has_admission_result():
        second_round_admitted = (applicant.admission_result.is_final_admitted and (not applicant.admission_result.is_admitted))

    if not second_round_admitted:
        raise Http404

    admission_result = applicant.admission_result

    Log.create("view confirmation second round - id: %d, from: %s" %
               (applicant.id, request.META['REMOTE_ADDR']),
               applicant_id=applicant.id,
               applicantion_id=applicant.submission_info.applicantion_id)

    return render_to_response('confirmation/second_round_confirmation.html',
                              { 'applicant': applicant,
                                'admission_result': admission_result })


@submitted_applicant_required
def show_confirmation_second_round(request):
    applicant = request.applicant
    return render_confirmation_form_second_round(request, applicant)

@login_required
def admin_show_confirmation_second_round(request, app_id):
    applicant = get_object_or_404(Applicant, pk=app_id)
    return render_confirmation_form_second_round(request, applicant)


#
# ROUND2 ADMISSION
#

class Round2ConfirmationForm(ModelForm):
    class Meta:
        model = Round2ApplicantConfirmation
        exclude = ('applicant',)

@submitted_applicant_required
def confirm_round2(request):
    """
    Obsoleted
    """
    return HttpResponseForbidden()

    applicant = request.applicant
    
    if not applicant.submission_info.doc_reviewed_complete:
        return HttpResponseForbidden()

    if round2_confirmation_deadline_passed():
        return HttpResponseForbidden()

    try:
        confirmation = applicant.round2_confirmation
        has_submitted = True
    except Round2ApplicantConfirmation.DoesNotExist:
        confirmation = Round2ApplicantConfirmation()
        confirmation.applicant = applicant
        has_submitted = False

    if request.method == 'POST':
        if 'cancel' in request.POST:
            if has_submitted:
                request.session['notice'] = 'ตัวเลือกการยืนยันไม่ถูกแก้ไข'
            else:
                request.session['notice'] = 'ไม่ยืนยันการขอรับพิจารณาในการสมัครโครงการรับตรง (รอบที่ 2)'
            return HttpResponseRedirect(reverse('status-index'))
        else:
            form = Round2ConfirmationForm(request.POST, instance=confirmation)
            if form.is_valid():
                confirmation = form.save()

                Log.create("Confirmation round 2 - id: %d, from: %s, choices: %d,%d" %
                           (applicant.id, 
                            request.META['REMOTE_ADDR'],
                            confirmation.is_confirmed,
                            confirmation.is_applying_for_survey_engr),
                           applicant_id=applicant.id,
                           applicantion_id=applicant.submission_info.applicantion_id)

                request.session['notice'] = 'จัดเก็บตัวเลือกการยืนยันเรียบร้อย'
                return HttpResponseRedirect(reverse('status-index'))
    else:
        form = Round2ConfirmationForm(instance = confirmation)


    return render_to_response('confirmation/round2_confirmation.html',
                              { 'applicant': applicant,
                                'form': form,
                                'has_submitted': has_submitted })


