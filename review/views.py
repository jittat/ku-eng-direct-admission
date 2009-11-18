# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from application.models import Applicant
from application.models import SubmissionInfo

def find_basic_statistics():
    return {
        'app_registered': Applicant.objects.count(),
        'app_submitted': SubmissionInfo.objects.count()
        }


@login_required
def index(request):
    stat = find_basic_statistics()
    return render_to_response("review/index.html",
                              { 'stat': stat })

