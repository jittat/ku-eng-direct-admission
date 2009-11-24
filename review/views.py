# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django import forms

from application.models import Applicant, Education
from application.models import SubmissionInfo

from commons.email import send_validation_successful_by_email
from commons.email import send_validation_error_by_email

from models import ReviewField, ReviewFieldResult

def find_basic_statistics():
    stat = {
        'app_registered': Applicant.objects.count(),
        'app_submitted': SubmissionInfo.objects.count(),
        'app_submitted_postal': 
        Applicant.objects.filter(doc_submission_method=Applicant.SUBMITTED_BY_MAIL).count(),
        'app_submitted_online': 
        Applicant.objects.filter(doc_submission_method=Applicant.SUBMITTED_ONLINE).count(),
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
    ticket_number = forms.IntegerField()
    verification_number = forms.CharField(required=False)

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
            submission_info = SubmissionInfo.find_by_ticket_number(str(ticket))
            if submission_info!=None:
                try:
                    applicants = [submission_info.applicant]
                except:
                    pass

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
        if submission_info.has_received_doc():
            submission_info.doc_received_at = None
        else:
            submission_info.doc_received_at = datetime.now()
        submission_info.save()

        return render_to_response("review/include/doc_received_status_block.html",
                                  {'has_received_doc':
                                       submission_info.has_received_doc()})

    return HttpResponseForbidden()


def get_applicant_doc_name_list(applicant):
    names = []
    names.append('image')
    names.append('id_card')
    names.append('edu_certificate')
    if applicant.education.uses_gat_score:
        names.append('gat')
        names.append('pat1')
        names.append('pat3')
    else:
        names.append('anet')
    names.append('deposite')
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
def review_document(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    submission_info = applicant.submission_info

    if not submission_info.can_be_reviewed():
        request.session['notice'] = 'ยังไม่สามารถตรวจสอบเอกสารได้เนื่องจากยังไม่พ้นช่วงเวลาสำหรับการแก้ไข'
        return HttpResponseRedirect(reverse('review-ticket'))

    if request.method=='POST':
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
            return HttpResponseRedirect(reverse('review-ticket'))
    else:
        data = prepare_applicant_review_data(applicant)
        
    return render_to_response("review/show.html",
                              { 'applicant': applicant,
                                'submission_info': submission_info,
                                'review_data': data })

