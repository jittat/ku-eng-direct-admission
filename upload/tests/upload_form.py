# -*- coding: utf-8 -*-
import os.path

from django.core import mail
from django.test import TestCase, TransactionTestCase
from django.conf import settings

from application.models import Applicant, Registration
from commons import email

from application.tests.info_forms import FormsTestCaseBase
from review.tests.review import *

def get_uploading_file(filename):
    full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             filename)
    return open(full_path)


class UploadTestCaseBase(FormsTestCaseBase):

    DOC_FIELDS = [
        'nat_id',
        'picture',
        'edu_certificate',
        'gat_score',
        'pat1_score',
        'pat3_score',
        'app_fee_doc',
        ]

    def _upload_one_field(self, url, check=True):
        response = self.client.post(url,
                                    {'uploaded_file': 
                                     get_uploading_file('data/image.png'),
                                     'submit': 'Upload'})
        self.assertRedirects(response,'/doc/')
        return self.client.get('/doc/')

    def _upload_all_fields(self):
        for f in UploadTestCase.DOC_FIELDS:
            response = self._upload_one_field('/doc/upload/%s/' % (f,))
            self.assertContains(response, '/doc/preview/%s' % (f,))



class UploadTestCase(UploadTestCaseBase):

    def test_seeing_upload_fields(self):
        response = self._fill_forms_upto_online_doc_upload_form()
        self.assertContains(response, 'picture')
        self.assertContains(response, 'edu_certificate')
        self.assertContains(response, 'nat_id')

    def test_uploading_one_field(self):
        self._fill_forms_upto_online_doc_upload_form()
        response = self._upload_one_field('/doc/upload/nat_id/')
        self.assertContains(response, '/doc/preview/nat_id')


    def test_uploading_all_fields(self):
        self._fill_forms_upto_online_doc_upload_form()
        self._upload_all_fields()


    def test_submit_on_incomplete_upload(self):
        self._fill_forms_upto_online_doc_upload_form()
        response = self._upload_one_field('/doc/upload/nat_id/')
        self.assertContains(response, '/doc/preview/nat_id')
        
        response = self.client.post('/doc/submit/',
                                    {'submit': 'ส่งใบสมัคร'})
        self.assertContains(response,'doc-error')


    def test_submit_on_complete_upload_and_confirm(self):
        self._fill_forms_upto_online_doc_upload_form()
        self._upload_all_fields()
        response = self.client.post('/doc/submit/',
                                    {'submit': 'ส่งใบสมัคร'})
        self.assertRedirects(response,'/doc/confirm/')

        response = self.client.post('/doc/confirm/',
                                    {'submit': 'ยืนยัน'})
        self.assertTemplateUsed(response,'upload/submission_success.html')
        self.assertEquals(len(mail.outbox),1)

    def test_upload_on_submitted_applicant(self):
        self._fill_forms_upto_online_doc_upload_form()
        self._upload_all_fields()
        response = self.client.post('/doc/submit/',
                                    {'submit': 'ส่งใบสมัคร'})
        self.assertRedirects(response,'/doc/confirm/')

        response = self.client.post('/doc/confirm/',
                                    {'submit': 'ยืนยัน'})
        self.assertTemplateUsed(response,'upload/submission_success.html')

        self.client.get('/apply/logout/')

        response = self._login_required(check=False)
        self.assertRedirects(response,'/apply/status/')
        
        response = self.client.post('/doc/upload/nat_id/',
                                    {'uploaded_file': 
                                     get_uploading_file('data/image.png'),
                                     'submit': 'Upload'})
        self.assertEquals(response.status_code, 403)


class ResubmissionTestCase(ReviewTestCaseBase, UploadTestCaseBase):

    def test_no_resubmission_link_for_unreviewed_applicant(self):
        self._login_required(SOMCHAI_EMAIL, SOMCHAI_PASSWORD)
        response = self.client.get('/apply/status/')
        self.assertNotContains(response, '/upload/update/')
        

    def test_no_resubmission_link_for_complete_reviewed_applicant(self):
        self._admin_login_required()

        self.client.post('/review/show/1/',
                         ALL_PASSED_REVIEW_FORM_DATA_GATPAT)

        self._login_required(SOMCHAI_EMAIL, SOMCHAI_PASSWORD)
        response = self.client.get('/apply/status/')
        self.assertNotContains(response, '/doc/update/')
        

    def test_resubmission_link_for_incomplete_reviewed_applicant(self):
        self._review_somchai()
        self._login_required(SOMCHAI_EMAIL, SOMCHAI_PASSWORD)
        response = self.client.get('/apply/status/')
        self.assertContains(response, '/doc/update/')


    def test_doc_update_page_inaccessible_for_complete_review(self):
        self._review_somchai(ALL_PASSED_REVIEW_FORM_DATA_GATPAT)
        response = self._goto_update_page()
        self.assertNotEquals(response.status_code, 200)


    def test_doc_update_page_inaccessible_for_unreview(self):
        response = self._goto_update_page()
        self.assertNotEquals(response.status_code, 200)


    def test_doc_updata_page_shows_only_incomplete_fields(self):
        self._review_somchai()
        response = self._goto_update_page()
        self.assertContains(response, 'app_fee_doc')
        self.assertNotContains(response, 'nat_id')
        self.assertNotContains(response, 'picture')
        self.assertNotContains(response, 'edu_certificate')


    def test_upload_for_resubmitted_field(self):
        self._review_somchai()
        self._goto_update_page()
        response = self.client.post('/doc/upload/app_fee_doc/',
                                    {'uploaded_file': 
                                     get_uploading_file('data/image.png'),
                                     'submit': 'Upload'})
        self.assertRedirects(response, '/doc/update/')


    def test_upload_for_completed_field(self):
        self._review_somchai()
        self._goto_update_page()
        response = self.client.post('/doc/upload/nat_id/',
                                    {'uploaded_file': 
                                     get_uploading_file('data/image.png'),
                                     'submit': 'Upload'})
        self.assertEquals(response.status_code, 403)


    def test_resubmision(self):
        self._review_somchai_and_resubmit()

        response = self.client.get('/apply/status/')
        self.assertContains(response, 'คุณได้ส่งหลักฐานเพิ่มเติมแล้ว')
        self.assertNotContains(response, '/doc/update/')

    def test_review_success_after_resubmision(self):
        self._review_somchai_and_resubmit()

        response = self.client.get('/apply/status/')
        self.assertContains(response, 'คุณได้ส่งหลักฐานเพิ่มเติมแล้ว')
        self.assertNotContains(response, '/doc/update/')

        import time
        time.sleep(2)
        self._review_somchai(ALL_PASSED_REVIEW_FORM_DATA_GATPAT)

        response = self.client.get('/apply/status/')
        self.assertContains(response, 'ตรวจสอบเรียบร้อย')
        self.assertNotContains(response, '/doc/update/')

    def test_review_failed_after_resubmision(self):
        self._review_somchai_and_resubmit()

        response = self.client.get('/apply/status/')
        self.assertContains(response, 'คุณได้ส่งหลักฐานเพิ่มเติมแล้ว')
        self.assertNotContains(response, '/doc/update/')

        import time
        time.sleep(2)
        self._review_somchai(DEPOSITE_MISSING_REVIEW_FORM_DATA_GATPAT)

        response = self.client.get('/apply/status/')
        self.assertContains(response, 'แต่ยังมีข้อผิดพลาดอยู่')
        self.assertContains(response, '/doc/update/')

    # -------- helpers

    def _review_somchai(self, form_data=DEPOSITE_MISSING_REVIEW_FORM_DATA_GATPAT):
        self._admin_login_required()
        self.client.post('/review/show/1/',
                         form_data)
        
    def _goto_update_page(self, check=True):
        self._login_required(SOMCHAI_EMAIL, SOMCHAI_PASSWORD)
        
        self.client.get('/apply/status/')
        
        return self.client.get('/doc/update/')

    def _review_somchai_and_resubmit(self, check=True):
        self._review_somchai()
        if check:
            self.assertEquals(len(mail.outbox),1)
        self._goto_update_page()
        response = self.client.post('/doc/upload/app_fee_doc/',
                                    {'uploaded_file': 
                                     get_uploading_file('data/image.png'),
                                     'submit': 'Upload'})
        response = self.client.post('/doc/update/')
        if check:
            self.assertEquals(len(mail.outbox),2)
            self.assertRedirects(response, '/apply/status/')
        return response
        
