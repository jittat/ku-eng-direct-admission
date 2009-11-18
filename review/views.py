# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from django import forms

from application.models import Applicant
from application.models import SubmissionInfo

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

                for applicant in applicants:
                    match_ticket = (applicant.ticket_number()==ticket)
                    match_verinum = (
                        applicant.verification_number().startswith(verinum))
                    results.append({ 'ticket': match_ticket,
                                     'verinum': match_verinum })
                           
    else:
        form = ApplicantSearchByIDForm()

    return render_to_response("review/ticket_search.html",
                              { 'form': form,
                                'applicants_results': zip(applicants,results) })


