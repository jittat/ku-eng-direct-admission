from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import cache_page

from models import ReportCategory

@cache_page(60 * 5)
def list(request, page_id=None):
    report_categories = ReportCategory.objects.all()

    if page_id!=None:
        category = get_object_or_404(ReportCategory, pk=page_id)
        qualified_applicants = category.qualifiedapplicant_set.all()
    else:
        qualified_applicants = None

    return render_to_response("result/index.html",
                              { 'report_categories':
                                    report_categories,
                                'applicants':
                                    qualified_applicants,
                                'current_cat_id': int(page_id) })


