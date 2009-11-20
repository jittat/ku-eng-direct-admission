# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django import forms

from application.models import Applicant
from application.models import SubmissionInfo

from models import ReviewField, ReviewFieldResult

def find_basic_statistics():
    return {
        'app_registered': Applicant.objects.count(),
        'app_submitted': SubmissionInfo.objects.count(),
        'app_submitted_postal': 
        Applicant.objects.filter(doc_submission_method=Applicant.SUBMITTED_BY_MAIL).count(),
        'app_submitted_online': 
        Applicant.objects.filter(doc_submission_method=Applicant.SUBMITTED_ONLINE).count(),
        }

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

                if ('search-and-show' in request.POST) and (len(applicants)==1):
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
                                'applicants_results': zip(applicants,results) })

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

        return render_to_response("review/include/doc_received_status.html",
                                  {'has_received_doc':
                                       submission_info.has_received_doc()})

    return HttpResponseForbidden()


def prepare_applicant_review_data(applicant):
    fields = ReviewField.get_all_fields()
    app_fields = []
    app_fields.append(fields['image'])
    app_fields.append(fields['id_card'])
    app_fields.append(fields['edu_certificate'])
    if applicant.education.uses_gat_score:
        app_fields.append(fields['gat'])
        app_fields.append(fields['pat1'])
        app_fields.append(fields['pat3'])
    else:
        app_fields.append(fields['anet'])
    app_fields.append(fields['deposite'])
    app_fields.append(fields['abroad_edu_certificate'])
    return app_fields


@login_required
def review_document(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    fields = prepare_applicant_review_data(applicant)

    return render_to_response("review/show.html",
                              { 'applicant': applicant,
                                'fields': fields })

