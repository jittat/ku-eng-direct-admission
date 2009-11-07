from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

def redirect_to_index(request):
    # clear user session
    if 'applicant_id' in request.session:
        del request.session['applicant_id']
    # go back to front page, will be changed later
    return HttpResponseRedirect(reverse(settings.INDEX_PAGE))


def admin_email():
    admin = settings.ADMINS[0]
    return admin[1]
