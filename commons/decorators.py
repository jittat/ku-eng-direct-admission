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
                         select_related(depth=1).
                         get(pk=request.session['applicant_id']))
        except Applicant.DoesNotExist:
            return redirect_to_index(request)

        request.applicant = applicant
        return view_function(request, *args, **kwargs)

    return decorate
