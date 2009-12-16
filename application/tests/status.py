# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase, TransactionTestCase
from django.conf import settings

from application.models import Applicant

SOMCHAI_EMAIL = "somchai@thailand.com"
SOMCHAI_PASSWORD = "coykx"

class StatusTestCase(TransactionTestCase):

    fixtures = ['submissions']

    def setUp(self):
        # remove submission dealine
        settings.SUBMISSION_DEADLINE = None

    def test_app_can_see_link_edu_info_change_before_grace_period(self):
        old_grace_period_end = settings.SUBMISSION_CHANGE_GRACE_PERIOD_END
        settings.SUBMISSION_CHANGE_GRACE_PERIOD_END = (
            datetime.now() + timedelta(1))

        applicant = Applicant.get_applicant_by_email(SOMCHAI_EMAIL)
        applicant.submission_info.submitted_at = (
            settings.SUBMISSION_CHANGE_GRACE_PERIOD_END
            - timedelta(1)
            )
        applicant.submission_info.save()

        self._login_required(SOMCHAI_EMAIL,SOMCHAI_PASSWORD)

        response = self.client.get('/apply/status/')
        self.assertContains(response, "id_edu-update-button")
        self.assertContains(response, "id_majors-update-button")

        settings.SUBMISSION_CHANGE_GRACE_PERIOD_END = old_grace_period_end

    def test_app_cannot_view_edu_info_change_after_grace_period(self):
        old_grace_period_end = settings.SUBMISSION_CHANGE_GRACE_PERIOD_END
        settings.SUBMISSION_CHANGE_GRACE_PERIOD_END = (
            datetime.now() - timedelta(1))

        self._login_required(SOMCHAI_EMAIL,SOMCHAI_PASSWORD)

        response = self.client.get('/apply/update/education')
        self.assertTemplateNotUsed(response, 
                                   "application/update/education.html")
        
        settings.SUBMISSION_CHANGE_GRACE_PERIOD_END = old_grace_period_end


    def test_app_cannot_see_edu_info_change_link_after_grace_period(self):
        old_grace_period_end = settings.SUBMISSION_CHANGE_GRACE_PERIOD_END
        settings.SUBMISSION_CHANGE_GRACE_PERIOD_END = (
            datetime.now() - timedelta(1))

        self._login_required(SOMCHAI_EMAIL,SOMCHAI_PASSWORD)

        response = self.client.get('/apply/status/')
        self.assertNotContains(response, "id_edu-update-button")
        self.assertContains(response, "id_majors-update-button")

        settings.SUBMISSION_CHANGE_GRACE_PERIOD_END = old_grace_period_end


    # ---------------------------------

    def _login_required(self,email, password):
        response = self.client.post('/apply/login/',
                                    {'email': email,
                                     'password': password })

