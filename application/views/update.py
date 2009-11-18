# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from commons.decorators import submitted_applicant_required

from application.views.form_views import prepare_major_form
from application.forms.handlers import handle_major_form

@submitted_applicant_required
def update_majors(request):
    applicant = request.applicant

    if request.method == 'POST': 

        if 'cancel' not in request.POST:

            result, major_list, errors = handle_major_form(request)

            if result:
                request.session['notice'] = 'การแก้ไขอันดับสาขาวิชาเรียบร้อย'
                return HttpResponseRedirect(reverse('status-index'))

        else:
            request.session['notice'] = 'ยกเลิกการแก้ไขอันดับสาขาวิชา'
            return HttpResponseRedirect(reverse('status-index'))

        pref_ranks = MajorPreference.major_list_to_major_rank_list(major_list)
        form_data = prepare_major_form(applicant, pref_ranks, errors)

    else:
        if applicant.has_major_preference():
            pref_ranks = applicant.preference.to_major_rank_list()
        else:
            pref_ranks = [None] * len(majors)

        form_data = prepare_major_form(applicant, pref_ranks)

    # add step info
    form_data['step_name'] = 'แก้ไขอันดับสาขาวิชา'
    form_data['can_log_out'] = True
    return render_to_response('application/update/majors.html',
                              form_data)
