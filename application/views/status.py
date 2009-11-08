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
            return redirect_to_applicant_first_page

    return decorate


@submitted_applicant_required
def index(request):
    return render_to_response("application/status/index.html",
                              { 'applicant': request.applicant })


@submitted_applicant_required
def show(request):
    return render_to_response("application/status/show.html",
                              { 'applicant': request.applicant })

