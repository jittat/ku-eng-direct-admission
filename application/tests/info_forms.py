# -*- coding: utf-8 -*-

from django.core import mail
from django.test import TestCase, TransactionTestCase

from django.conf import settings

from application.models import Applicant, Registration
from commons import email

from helpers import ApplicantPreparation

class InfoFormsTestCase(TransactionTestCase):

    fixtures = ['major', 'gatpat-dates']

    def setUp(self):
        self.app_prep = ApplicantPreparation()
        self.applicant, self.password = self.app_prep.create_applicant()
        self.email = self.applicant.email


    def test_user_can_login(self):
        self._login_required()


    PERSONAL_FORM_DATA = {
        'national_id': '1234567890123',
        'birth_date_day': '1',
        'birth_date_month': '1',
        'birth_date_year': '1990',
        'ethnicity': u'ไทย',
        'nationality': u'ไทย',
        'phone_number': u'081-111-2222 ต่อ 1234'
        }

    ADDRESS_FORM_DATA = {
        'contact-city':'ลำลูกกา',
        'contact-district':'คูคต',
        'contact-number':'74/13',
        'contact-phone_number':'029948402',
        'contact-postal_code':'12130',
        'contact-province':'ปทุมธานี',
        'contact-road':'พหลโยธิน',
        'contact-village_name':'',
        'contact-village_number':'10',
        'home-city':'ลำลูกกา',
        'home-district':'คูคต',
        'home-number':'74/13',
        'home-phone_number':'029948402',
        'home-postal_code':'12130',
        'home-province':'ปทุมธานี',
        'home-road':'พหลโยธิน',
        'home-village_name':'',
        'home-village_number':'10',
        'submit':'เก็บข้อมูล',
        }

    EDU_FORM_DATA_GATPAT = {
        'anet':'10',
        'gat':'100',
        'gat_date':'1',
        'gpax':'3.45',
        'has_graduated':'True',
        'pat1':'200',
        'pat1_date':'2',
        'pat3':'300',
        'pat3_date':'3',
        'school_city':'เมือง',
        'school_name':'สาธิต',
        'school_province':'จันทบุรี',
        'submit':'เก็บข้อมูล',
        'uses_gat_score':'True',
        }

    MAJOR_RANK_FORM_DATA = {
        'major_1':'3',
        'major_10':'--',
        'major_11':'--',
        'major_12':'--',
        'major_13':'--',
        'major_2':'4',
        'major_3':'--',
        'major_4':'--',
        'major_5':'6',
        'major_6':'5',
        'major_7':'2',
        'major_8':'--',
        'major_9':'1',
        'submit':'เก็บข้อมูล',
        }

    def _test_personal_form(self):
        self._login_required()
        self._personal_info_required()

    def _test_address_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()

    def test_edu_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()

    def test_majors_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()

    def test_postal_submission_confirm(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()
        self._submit_postal_doc_confirm_required()


    def test_online_submission_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()
        self._online_doc_upload_form_required()


    def test_wrong_jump_to_online_submission_form(self):
        self._login_required()
        self._personal_info_required()
        response = self.client.get('/doc/')
        self.assertNotEqual(response.status_code, 200)

    # helpers method

    def _login_required(self):
        response = self.client.post('/apply/login/',
                                    {'email': self.email,
                                     'password': self.password})
        
        self.assertRedirects(response,'/apply/personal/')

    def _personal_info_required(self):
        response = self.client.post('/apply/personal/',
                                    InfoFormsTestCase.PERSONAL_FORM_DATA)
        self.assertRedirects(response,'/apply/address/')
                
    def _address_info_required(self):
        response = self.client.post('/apply/address/',
                                    InfoFormsTestCase.ADDRESS_FORM_DATA)
        self.assertRedirects(response,'/apply/education/')
        
    def _edu_info_required(self):
        response = self.client.post('/apply/education/',
                                    InfoFormsTestCase.EDU_FORM_DATA_GATPAT)
        self.assertRedirects(response,'/apply/majors/')

    def _major_ranks_info_required(self):
        response = self.client.post('/apply/majors/',
                                    InfoFormsTestCase.MAJOR_RANK_FORM_DATA)
        self.assertRedirects(response,'/apply/doc_menu/')

    def _submit_postal_doc_confirm_required(self):
        response = self.client.get('/apply/confirm/')
        self.assertEqual(response.status_code, 200)

    def _online_doc_upload_form_required(self):
        response = self.client.get('/doc/')
        self.assertEqual(response.status_code, 200)

