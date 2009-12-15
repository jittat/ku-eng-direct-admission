from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from utils import redirect_to_index, submission_deadline_passed
from application.models import Applicant

from django.conf import settings

def within_submission_deadline(view_function):
    def decorate(request, *args, **kwargs):
        if submission_deadline_passed():
            return render_to_response("commons/closed.html")
        return view_function(request, *args, **kwargs)

    return decorate


def applicant_required(view_function):
    """
    Returns a view function that checks if the requesting user is a
    valid applicant.
    """
    def decorate(request, *args, **kwargs):
        if not 'applicant_id' in request.session:
            return redirect_to_index(request)
        try:
            applicant = (Applicant.objects.
                         get(pk=request.session['applicant_id']))
        except Applicant.DoesNotExist:
            return redirect_to_index(request)

        request.applicant = applicant
        return view_function(request, *args, **kwargs)

    return decorate


def active_applicant_required(view_function):
    """
    returns a view function that checks if the applicant has submitted
    the application, otherwise redirect to the applicant first page.
    """
    @applicant_required
    def decorate(request, *args, **kwargs):
        if not request.applicant.is_submitted:
            return view_function(request, *args, **kwargs)
        else:
            return redirect_to_index(request)

    return decorate


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
            return redirect_to_index(request)

    return decorate


def active_applicant_required_or_update(view_function):
    """
    returns a view function that checks if the applicant has submitted
    the application, otherwise redirect to the applicant first page.
    """
    @applicant_required
    def decorate(request, update, *args, **kwargs):
        if (not request.applicant.is_submitted) and (not update):
            # not submitted applicant, not update
            return view_function(request, *args, **kwargs)
        elif request.applicant.is_submitted and update:
            # submitted applicant, update
            return view_function(request, *args, **kwargs)
        else:
            return redirect_to_index(request)

    return decorate


