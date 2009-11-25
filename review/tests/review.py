# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase, TransactionTestCase

from django.conf import settings

from commons import email
from application.models import Applicant

SOMCHAI_EMAIL = "somchai@thailand.com"
SOMCHAI_PASSWORD = "coykx"

SOMYING_EMAIL = "somying@ku.ac.th"
SOMYING_PASSWORD = "bgchp"

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'testadmin'

ALL_PASSED_REVIEW_FORM_DATA = {
    'abroad_edu_certificate-applicant_note':'',
    'abroad_edu_certificate-internal_note':'',
    'app_fee_doc-applicant_note':'',
    'app_fee_doc-internal_note':'',
    'app_fee_doc-is_passed':'on',
    'edu_certificate-applicant_note':'',
    'edu_certificate-internal_note':'',
    'edu_certificate-is_passed':'on',
    'nat_id-applicant_note':'',
    'nat_id-internal_note':'',
    'nat_id-is_passed':'on',
    'picture-applicant_note':'',
    'picture-internal_note':'',
    'picture-is_passed':'on',
    'anet_score-applicant_note':'',
    'anet_score-internal_note':'',
    'anet_score-is_passed':'on',
    'submit':'เก็บข้อมูล',
    }

DEPOSITE_MISSING_REVIEW_FORM_DATA = {
    'abroad_edu_certificate-applicant_note':'',
    'abroad_edu_certificate-internal_note':'',
    'app_fee_doc-applicant_note':'หมายเลขไม่มี',
    'app_fee_doc-internal_note':'',
    'edu_certificate-applicant_note':'',
    'edu_certificate-internal_note':'',
    'edu_certificate-is_passed':'on',
    'nat_id-applicant_note':'',
    'nat_id-internal_note':'',
    'nat_id-is_passed':'on',
    'picture-applicant_note':'',
    'picture-internal_note':'',
    'picture-is_passed':'on',
    'anet_score-applicant_note':'',
    'anet_score-internal_note':'',
    'anet_score-is_passed':'on',
    'submit':'เก็บข้อมูล',
    }

class ReviewTestCase(TransactionTestCase):

    fixtures = ['submissions', 'admin_user', 'review_field']


    def setUp(self):
        # make sure the when testing, the app is using django's email
        # system.
        from django.core.mail import send_mail

        email.send_mail = send_mail 

        self.org_email_setting = settings.FAKE_SENDING_EMAIL
        settings.FAKE_SENDING_EMAIL = False


    def tearDown(self):
        settings.FAKE_SENDING_EMAIL = self.org_email_setting


    def test_doc_received_status_display_changed_after_admin_update(self):
        self._login_required(SOMYING_EMAIL,SOMYING_PASSWORD)
        response = self.client.get('/apply/status/')
        self.assertContains(response,"ยังไม่ได้รับ")

        self._admin_login_required()

        self.client.get('/review/received/toggle/2/')
        self.client.get('/accounts/logout/')

        self._login_required(SOMYING_EMAIL,SOMYING_PASSWORD)
        response = self.client.get('/apply/status/')
        self.assertNotContains(response,"ยังไม่ได้รับ")   


    def test_link_edu_info_update_removed_after_app_gets_reviewed(self):
        self._admin_login_required()

        self.client.post('/review/show/2/',
                         ALL_PASSED_REVIEW_FORM_DATA)

        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')
        self.assertNotContains(response, "id_edu-update-button")


    def test_app_cannot_edit_edu_info_after_getting_reviewed(self):
        self._admin_login_required()

        self.client.post('/review/show/2/',
                         ALL_PASSED_REVIEW_FORM_DATA)

        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/update/education')
        self.assertTemplateNotUsed(response, 
                                   "application/update/education.html")


    def test_review_status_update_successful(self):
        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')
        self.assertNotContains(response, "ตรวจสอบเรียบร้อย")

        self._admin_login_required()

        self.client.post('/review/show/2/',
                         ALL_PASSED_REVIEW_FORM_DATA)

        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')

        self.assertContains(response, "ตรวจสอบเรียบร้อย")

    def test_review_status_update_failed(self):
        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')
        self.assertNotContains(response, "ตรวจสอบเรียบร้อย")

        self._admin_login_required()

        response = self.client.post('/review/show/2/',
                                    DEPOSITE_MISSING_REVIEW_FORM_DATA)

        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')

        self.assertNotContains(response, "ตรวจสอบเรียบร้อย")
        self.assertContains(response, "หลักฐานใบนำฝาก")
        self.assertContains(response, "หมายเลขไม่มี")

    # ---------------------------------

    def _login_required(self,email, password):
        response = self.client.post('/apply/login/',
                                    {'email': email,
                                     'password': password })
        
        self.assertRedirects(response,'/apply/status/')
        return response

    def _admin_login_required(self):
        response = self.client.post('/accounts/login/',
                                    {'username': ADMIN_USERNAME,
                                     'password': ADMIN_PASSWORD,
                                     'next': '/review/'})
        self.assertRedirects(response, '/review/')
