from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import ReportCategory

RESULT_ID_FIELD = 0
RESULT_NAME_FIELD = 1
RESULT_ENABLED_FIELD = 2
RESULT_TEMPLATE_FILED = 3

RESULT_ID_MAP = dict([(r[RESULT_NAME_FIELD], r[RESULT_ID_FIELD])
                      for r in settings.RESULT_SETS])
RESULT_ID_INDEX = dict([(r[RESULT_ID_FIELD],i)
                        for r,i 
                        in zip(settings.RESULT_SETS, range(len(settings.RESULT_SETS)))])

def index(request):
    result_set_name = settings.RESULT_SETS[0][RESULT_NAME_FIELD]
    return HttpResponseRedirect(reverse('result-set-index', 
                                        args=[result_set_name]))

@cache_page(60 * 5)
def list(request, result_set_name=None, page_id=None):
    if result_set_name==None:
        result_set_name = settings.RESULT_SETS[0][RESULT_NAME_FIELD]

    print result_set_name

    try:
        result_set_id = RESULT_ID_MAP[result_set_name]
    except:
        return HttpResponseForbidden()

    result_set = settings.RESULT_SETS[RESULT_ID_INDEX[result_set_id]]

    if not result_set[RESULT_ENABLED_FIELD]:
        return HttpResponseForbidden()

    report_categories = (ReportCategory.objects
                         .filter(result_set_id=result_set_id).all())

    if page_id!=None:
        category = get_object_or_404(ReportCategory, pk=page_id)
        qualified_applicants = category.qualifiedapplicant_set.all()
    else:
        qualified_applicants = None
        page_id = 0

    template_name = result_set[RESULT_TEMPLATE_FILED]

    return render_to_response(template_name,
                              { 'report_categories':
                                    report_categories,
                                'applicants':
                                    qualified_applicants,
                                'current_cat_id': int(page_id),
                                'current_result_set_name': result_set_name })
