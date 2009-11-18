from django.http import HttpResponseRedirect
from utils import redirect_to_index
from application.models import Applicant

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


