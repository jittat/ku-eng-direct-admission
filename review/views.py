# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django import forms

from commons.utils import serve_file

from application.models import Applicant, Education
from application.models import SubmissionInfo
from upload.models import AppDocs
from manual.models import AdminEditLog

from commons.email import send_validation_successful_by_email
from commons.email import send_validation_error_by_email
from commons.email import send_resubmission_reminder_by_email

from models import ReviewField, ReviewFieldResult
from supplement.models import Supplement

def find_basic_statistics():
    manual_app_count = Applicant.objects.filter(is_offline=True).count()
    submitted_manual_app_count = Applicant.get_submitted_offline_applicants().count()
    total_submitted_app_count = SubmissionInfo.objects.count()
    stat = {
        'online_app_registered': 
        Applicant.objects.count() - manual_app_count,
        'app_qualified': SubmissionInfo.get_qualified_submissions().count(),
        'app_submitted': total_submitted_app_count,
        'online_app_submitted':
            total_submitted_app_count - submitted_manual_app_count,
        'app_submitted_postal':
            Applicant.objects.filter(doc_submission_method=Applicant.SUBMITTED_BY_MAIL).count(),
        'app_submitted_online':
            Applicant.objects.filter(doc_submission_method=Applicant.SUBMITTED_ONLINE).count(),
        'app_submitted_offline':
            submitted_manual_app_count,
        'app_received': {
            'reviewed': SubmissionInfo.objects.filter(doc_received_at__isnull=False).filter(has_been_reviewed=True).count(),
            'not_reviewed': SubmissionInfo.objects.filter(doc_received_at__isnull=False).filter(has_been_reviewed=False).count(),
            }
        }
    stat['app_received']['total'] = (
        stat['app_received']['reviewed'] +
        stat['app_received']['not_reviewed'])
    return stat

@login_required
def index(request):
    stat = find_basic_statistics()
    return render_to_response("review/index.html",
                              { 'stat': stat })

class ApplicantSearchByIDForm(forms.Form):
    ticket_number = forms.IntegerField(required=False)
    full_name = forms.CharField(required=False)
    verification_number = forms.CharField(required=False)

def find_applicants(form):
    ticket = form.cleaned_data['ticket_number']
    verinum = form.cleaned_data['verification_number']
    full_name = form.cleaned_data['full_name']
    if ticket:
        submission_info = SubmissionInfo.find_by_ticket_number(str(ticket))
        if submission_info!=None:
            return [submission_info.applicant]
        else:
            return []
    elif full_name:
        # search by name
        applicants = []
        items = full_name.strip().split(' ')
        if items[0]!='':
            applicants = Applicant.objects.all()
            applicants = applicants.filter(first_name__contains=items[0])
            if len(items)>1 and items[1]!='':
                applicants = applicants.filter(last_name__contains=items[1])
            applicants = applicants.filter(is_submitted=True)
        return applicants
    else:
        return []

def put_minimal_info_to_applicants(applicants):

    def ticket_number(self):
        return '-'
    def verification_number(self):
        return '-'

    import new

    for applicant in applicants:
        applicant.ticket_number = new.instancemethod(ticket_number,applicant)
        applicant.verification_number = new.instancemethod(verification_number,applicant)
        applicant.is_submitted = False

@login_required
def verify_ticket(request):

    if 'notice' in request.session:
        notice = request.session['notice']
        del request.session['notice']
    else:
        notice = ''
    
    applicants = []
    results = []

    if request.method=='POST':
        form = ApplicantSearchByIDForm(request.POST)
        if form.is_valid():
            ticket = form.cleaned_data['ticket_number']
            verinum = form.cleaned_data['verification_number']

            applicants = find_applicants(form)

            # when there are too many results, put empty stub to
            # prevent huge database load.
            if (not type(applicants)==list) and (applicants.count()>20):
                put_minimal_info_to_applicants(applicants)

            if applicants != None and len(applicants) > 0:
                if (('search-and-show' in request.POST) 
                    and (len(applicants)==1) and
                    (applicants[0].submission_info.can_be_reviewed()) and
                    (not applicants[0].online_doc_submission())):
                    return HttpResponseRedirect(reverse('review-show',
                                                        args=[applicants[0].id]))

                for applicant in applicants:
                    match_ticket = (applicant.ticket_number()==str(ticket))
                    match_verinum = (
                        applicant.verification_number().startswith(verinum))
                    results.append({ 'ticket': match_ticket,
                                     'verinum': match_verinum })
    else:
        form = ApplicantSearchByIDForm()

    return render_to_response("review/ticket_search.html",
                              { 'form': form,
                                'notice': notice,
                                'applicants_results': zip(applicants,results) })


class ApplicantSearchForm(forms.Form):
    school_name = forms.CharField(label="โรงเรียน", required=False)

@login_required
def search(request):
    applicants = []
    display = {}
    applicant_count = 0
    if request.method=='POST':
        form = ApplicantSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['school_name']!='':
                educations = (Education.objects.filter(
                        school_name__contains=form.cleaned_data['school_name'])
                              .select_related(depth=1))
                applicant_count = educations.count()

                # only show the first 100
                educations = educations.all()[:200]

                for e in educations:
                    app = e.applicant
                    app.education = e
                    applicants.append(app)
                display['edu'] = True
    else:
        form = ApplicantSearchForm()

    return render_to_response("review/search.html",
                              { 'form': form,
                                'applicant_count': applicant_count,
                                'applicants': applicants,
                                'display': display })


@login_required
def toggle_received_status(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    submission_info = applicant.submission_info
    
    if not applicant.online_doc_submission():
        submission_info.toggle_doc_received_at()

        return render_to_response("review/include/doc_received_status_block.html",
                                  {'has_received_doc':
                                       submission_info.has_received_doc()})

    return HttpResponseForbidden()


def get_applicant_doc_name_list(applicant):
    names = []
    names.append('picture')
    names.append('nat_id')
    names.append('edu_certificate')
    if applicant.education.uses_gat_score:
        names.append('gat_score')
        names.append('pat1_score')
        names.append('pat3_score')
    else:
        names.append('anet_score')
    names.append('app_fee_doc')
    names.append('abroad_edu_certificate')
    return names


def prepare_applicant_review_results(applicant, names):
    submitted_review_results = (ReviewFieldResult.
                                get_applicant_review_results(applicant))
    result_dict = {}
    for result in submitted_review_results:
        field_id = result.review_field_id
        field = ReviewField.get_field_by_id(field_id)
        result_dict[field.short_name] = result

    # reorganize the results, add None result when needed
    review_results = []
    for n in names:
        if n in result_dict:
            review_results.append(result_dict[n])
        else:
            review_results.append(None)
    return review_results

def prepare_applicant_review_fields(names):
    return [ReviewField.get_field_by_short_name(n)
            for n in names]

class ReviewResultForm(forms.Form):
    is_passed = forms.BooleanField(required=False)
    applicant_note = forms.CharField(required=False)
    internal_note = forms.CharField(required=False)
    is_submitted = forms.BooleanField(required=False)

def prepare_applicant_forms(applicant, names, results, post_data=None):
    forms = []
    for n, res in zip(names, results):
        if res!=None:
            initial={'is_passed': res.is_passed,
                     'applicant_note': res.applicant_note,
                     'internal_note': res.internal_note,
                     'is_submitted': True }
        else:
            initial=None
        forms.append(ReviewResultForm(post_data,
                                      prefix=n,
                                      initial=initial))
    return forms

def build_review_data(fields, results, forms):
    data = [ { 'field': field,
               'result': result,
               'form': form } 
             for field, result, form 
             in zip(fields, results, forms) ]

    return data

def prepare_applicant_review_data(applicant):
    field_names = get_applicant_doc_name_list(applicant)
    fields = prepare_applicant_review_fields(field_names)
    results = prepare_applicant_review_results(applicant, field_names)
    forms = prepare_applicant_forms(applicant, field_names, results)
    return build_review_data(fields, results, forms)

@login_required
def review_document(request, applicant_id, return_to_manual=False):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    submission_info = applicant.submission_info

    if not submission_info.can_be_reviewed():
        request.session['notice'] = 'ยังไม่สามารถตรวจสอบเอกสารได้เนื่องจากยังไม่พ้นช่วงเวลาสำหรับการแก้ไข'
        return HttpResponseRedirect(reverse('review-ticket'))

    if (request.method=='POST') and ('submit' in request.POST):
        # auto set received flag
        submission_info.set_doc_received_at_now_if_not()

        field_names = get_applicant_doc_name_list(applicant)
        fields = prepare_applicant_review_fields(field_names)
        results = prepare_applicant_review_results(applicant, field_names)
        forms = prepare_applicant_forms(applicant, field_names, results, request.POST)

        error = False
        for f in forms:
            if not f.is_valid():
                error = True

        if not error:
            failed_fields = []

            for field, result, form in zip(fields, results, forms):
                if not result:
                    result = ReviewFieldResult()

                result.applicant_note = form.cleaned_data['applicant_note']
                result.internal_note = form.cleaned_data['internal_note']

                result.review_field = field
                result.applicant = applicant

                if (field.required) or (form.cleaned_data['is_submitted']):
                    result.is_passed = form.cleaned_data['is_passed']
                    if result.id!=None:
                        result.save(force_update=True)
                    else:
                        result.save(force_insert=True)

                    if not result.is_passed:
                        failed_fields.append((field,result))
                else:
                    if result.id!=None:
                        result.delete()

            submission_info.has_been_reviewed = True
            submission_info.doc_reviewed_at = datetime.now()
            submission_info.doc_reviewed_complete = (len(failed_fields)==0)
            submission_info.save()

            if submission_info.doc_reviewed_complete:
                send_validation_successful_by_email(applicant)
                request.session['notice'] = 'จัดเก็บและแจ้งผลการตรวจว่าผ่านกับผู้สมัครแล้ว'
            else:
                send_validation_error_by_email(applicant, failed_fields)
                request.session['notice'] = 'จัดเก็บและแจ้งผลการตรวจว่าหลักฐานไม่ผ่านกับผู้สมัครแล้ว'
            if not return_to_manual:
                return HttpResponseRedirect(reverse('review-ticket'))
            else:
                return HttpResponseRedirect(reverse('manual-index'))
    elif 'cancel' in request.POST:
        request.session['notice'] = 'ยกเลิกการตรวจสอบ ผลตรวจทุกอย่างคงเดิม'
        #print return_to_manual
        if not return_to_manual:
            return HttpResponseRedirect(reverse('review-ticket'))
        else:
            return HttpResponseRedirect(reverse('manual-index'))
    else:
        data = prepare_applicant_review_data(applicant)

    if applicant.online_doc_submission():
        appdocs = applicant.appdocs
    else:
        appdocs = None
        
    return render_to_response("review/show.html",
                              { 'applicant': applicant,
                                'appdocs': appdocs,
                                'submission_info': submission_info,
                                'review_data': data })


APPLICANTS_PER_PAGE = 200

def get_applicants_from_submission_infos(submission_infos):
    applicants = []
    for s in submission_infos:
        app = s.applicant
        app.submission_info = s
        applicants.append(app)
    return applicants


def get_applicants_using_update_review_time_diff(time_diff, review_status=None):
    where_condition = ("ADDTIME(`last_updated_at`,'%s') >= `doc_reviewed_at`" 
                       % time_diff)
    submission_infos = (SubmissionInfo
                        .objects
                        .extra(where=[where_condition])
                        .select_related(depth=1))
    if review_status!=None:
        submission_infos = (
            submission_infos.filter(doc_reviewed_complete=review_status))
    return get_applicants_from_submission_infos(submission_infos)


@login_required
def list_applicant(request, reviewed=True, pagination=True):
    applicants = []
    display = {}
    submission_infos = SubmissionInfo.objects.filter(doc_received_at__isnull=False).filter(has_been_reviewed=reviewed).select_related(depth=1)
    if reviewed:
        submission_infos = submission_infos.order_by('-doc_reviewed_at')
    else:
        submission_infos = submission_infos.order_by('doc_received_at')

    applicant_count = submission_infos.count()

    if pagination:
        max_page = (applicant_count + APPLICANTS_PER_PAGE -1) / APPLICANTS_PER_PAGE
        page = 1
        if 'page' in request.GET:
            try:
                page = int(request.GET['page'])
            except:
                page = 1
        if page < 1 or page > max_page:
            page = 1
    else:
        max_page = 1
        page = 1

    display_start = APPLICANTS_PER_PAGE * (page - 1) + 1
    display_end = APPLICANTS_PER_PAGE * page
    submission_infos = submission_infos.all()[display_start-1:display_end]
    display_count = len(submission_infos)

    # add resubmitted applicants
    if not reviewed:
        resubmitted_submission_infos = list(SubmissionInfo.get_unreviewed_resubmitted_submissions().select_related(depth=1).all())
        applicant_count += len(resubmitted_submission_infos)
        submission_infos = list(resubmitted_submission_infos) + list(submission_infos)
        display_count = len(submission_infos)
        display_end += len(resubmitted_submission_infos)

    applicants = get_applicants_from_submission_infos(submission_infos)

    display['ticket_number']=True
    display['doc_received_at']=True
    if reviewed==True:
        display['doc_reviewed_at']=True
        display['doc_reviewed_complete']=True


    return render_to_response("review/search.html",
                              { 'form': None,
                                'applicant_count': applicant_count,
                                'applicants': applicants,
                                'force_review_link': True,
                                'pagination': pagination,
                                'display_start': display_start,
                                'display_end': display_end,
                                'display_count': display_count,
                                'page': page,
                                'max_page': max_page,
                                'display': display })

@login_required
def list_applicants_with_supplements(request, time_diff=None, review_status=False):
    if time_diff == None:
        time_diff = '00:01:00'

    applicants = get_applicants_using_update_review_time_diff('00:01:00',
                                                              review_status)
    applicant_count = len(applicants)

    if review_status == None: 
        title = "รายชื่อผู้สมัครที่ยื่นหลักฐานเพิ่มหลังจากตรวจสอบแล้ว"
    elif review_status == False:
        title = "รายชื่อผู้สมัครที่หลักฐานไม่ผ่านที่ยื่นหลักฐานเพิ่มหลังจากตรวจสอบแล้ว"

    return render_to_response("review/list_applicants_with_supplements.html",
                              { 'form': None,
                                'list_title': title,
                                'applicant_count': applicant_count,
                                'applicants': applicants,
                                'force_review_link': True,
                                'display': 
                                { 'ticket_number': True,
                                  'doc_reviewed_at': True,
                                  'doc_reviewed_complete': True }})


@login_required
def list_incomplete_applicants(request, submission_method=None):
    submission_infos = (SubmissionInfo
                        .get_incomplete_submissions()
                        .select_related(depth=1))

    applicants = get_applicants_from_submission_infos(submission_infos)

    submission_method_name = ''
    if submission_method=='postal':
        submission_method_name = 'ที่สมัครออนไลน์แต่ส่งหลักฐานทางไปรษณีย์'
        applicants = [a for a in applicants 
                      if a.doc_submission_method==Applicant.SUBMITTED_BY_MAIL]
    elif submission_method=='offline':
        submission_method_name = 'ที่สมัครและส่งหลักฐานทางไปรษณีย์ (offline)'
        applicants = [a for a in applicants 
                      if a.doc_submission_method==Applicant.SUBMITTED_OFFLINE]
    elif submission_method=='online':
        submission_method_name = 'ที่สมัครและส่งหลักฐานออนไลน์ทั้งหมด'
        applicants = [a for a in applicants 
                      if a.doc_submission_method==Applicant.SUBMITTED_ONLINE]
        

    applicant_count = len(applicants)

    notice = ''

    can_send_reminder_emails = (request.user.is_superuser and 
                                submission_method != 'offline')

    if (request.method=='POST') and (can_send_reminder_emails):
        # form submission, now send e-mail
        for app in applicants:
            send_resubmission_reminder_by_email(app)
        notice = ("ส่งอีเมล์เตือน %d ฉบับแล้ว" % (applicant_count,))

    return render_to_response("review/list_incomplete_for_email.html",
                              { 'form': None,
                                'notice': notice,
                                'submission_method_name':
                                    submission_method_name,
                                'can_send_reminder_emails':
                                    can_send_reminder_emails,
                                'applicant_count': applicant_count,
                                'applicants': applicants,
                                'force_review_link': True,
                                'display':
                                    { 'ticket_number': True,
                                      'doc_reviewed_at': True,
                                      'doc_reviewed_complete': True }})

@login_required
def list_applicants_with_potential_edu_update_hazard(request):
    update_timestamps = {}
    review_timestamps = {}

    for education in Education.objects.all():
        update_timestamps[education.applicant_id] = education.updated_at

    for submission_info in SubmissionInfo.objects.all():
        review_timestamps[submission_info.applicant_id] = (
            submission_info.doc_reviewed_at)

    ten_minutes = timedelta(minutes=10)

    potential_list = []

    for app_id, review_timestamp in review_timestamps.iteritems():
        if app_id in update_timestamps:
            update_timestamp = update_timestamps[app_id]
            if ((update_timestamp != None) and (review_timestamp != None)
                and (update_timestamp + ten_minutes > review_timestamp)):
                potential_list.append((app_id, update_timestamp))

    all_applicants = [(Applicant.objects.get(pk=app_id), update_timestamp) 
                      for app_id, update_timestamp in potential_list]

    applicants = []
    for app, update_timestamp in all_applicants:
        if app.doc_submission_method != Applicant.SUBMITTED_OFFLINE:
            admin_log = AdminEditLog.objects.filter(applicant=app)
            is_manual_update = (len(admin_log) != 0)

            app.update_info = {
                'updated_at': update_timestamp,  # HACK: add field to display
                'is_manual_update': is_manual_update,
                }
            applicants.append(app)

    applicant_count = len(applicants)

    return render_to_response(
        "review/list_applicants_with_potential_edu_update_hazard.html",
        { 'form': None,
          'applicant_count': applicant_count,
          'applicants': applicants,
          'force_review_link': True,
          'display': 
          { 'ticket_number': True,
            'update_info': True,
            'doc_reviewed_at': True,
            'doc_reviewed_complete': True }})


############################################################
# views for displaying documents and supplements
#

IMG_MAX_HEIGHT = 450
IMG_MAX_WIDTH = 800

def cal_zoom_size(field):
    if field:
        height = field.height
        width = field.width
    else:
        height = 1
        width = 1

    hscale = float(height) / IMG_MAX_HEIGHT
    wscale = float(width) / IMG_MAX_WIDTH

    if (hscale > 1) or (wscale > 1):
        zoomable = True
        if hscale > wscale:
            new_h = IMG_MAX_HEIGHT
            new_w = int(width / hscale)
        else:
            new_h = int(height / wscale)
            new_w = IMG_MAX_WIDTH
    else:
        zoomable = False
        new_h, new_w = height, width

    return new_h, new_w, zoomable


@login_required
def doc_view(request, applicant_id, field_name):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    docs = applicant.get_applicant_docs_or_none()
    if not AppDocs.valid_field_name(field_name):
        return HttpResponseNotFound()

    field = docs.__getattribute__(field_name)

    ext = ''
    if field:
        filename = docs.__getattribute__(field_name).name
        if filename:
            name, ext = os.path.splitext(filename)
    if ext=='':
        ext = '.png'

    new_h, new_w, zoomable = cal_zoom_size(field)

    filename = '%s%s' % (field_name, ext)
    return render_to_response("review/doc_view.html",
                              { 'applicant': applicant,
                                'field_name': field_name,
                                'filename': filename,
                                'height': new_h,
                                'width': new_w,
                                'zoomable': zoomable })

@login_required
def supplement_view(request, supplement_id):
    supplement = get_object_or_404(Supplement, pk=supplement_id)

    name, ext = os.path.splitext(supplement.image.name)
    filename = '%s%s' % (supplement_id, ext)

    new_h, new_w, zoomable = cal_zoom_size(supplement.image)

    return render_to_response("review/supplement_view.html",
                              { 'applicant': supplement.applicant,
                                'supplement': supplement,
                                'filename': filename,
                                'height': new_h,
                                'width': new_w,
                                'zoomable': zoomable })


@login_required
def doc_img_view(request, applicant_id, filename):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    docs = applicant.get_applicant_docs_or_none()

    if docs!=None:
        field_name, ext = os.path.splitext(filename)

        if not AppDocs.valid_field_name(field_name):
            return HttpResponseNotFound()

        try:
            full_path = docs.__getattribute__(field_name).path

            if os.path.exists(full_path):
                return serve_file(full_path)
            else:
                return HttpResponseNotFound()
        except ValueError:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()


@login_required
def supplement_img_view(request, filename):
    fname, ext = os.path.splitext(filename)

    try:
        supplement_id = int(fname)
    except:
        return HttpResponseForbidden()

    supplement = get_object_or_404(Supplement, pk=supplement_id)

    try:
        full_path = supplement.image.path
        
        if os.path.exists(full_path):
            return serve_file(full_path)
        else:
            return HttpResponseNotFound()
    except ValueError:
        return HttpResponseNotFound()
