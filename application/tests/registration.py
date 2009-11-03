# _*_ encoding: utf-8 _*_

from django.core import mail
from django.test import TestCase, TransactionTestCase

from django.conf import settings

from application.models import Applicant

class RegistrationTestCase(TransactionTestCase):

    REGIS_DATA = {
        'first_name': u'สมชาย',
        'last_name': u'ใจดี',
        #'first_name': 'somchai',
        #'last_name': 'jaidee',
        'email': 'somchai@gmail.com',
        'email_confirmation': 'somchai@gmail.com'
        }

    def setUp(self):
        self.regis_data = dict(RegistrationTestCase.REGIS_DATA)

    def test_load_register_page(self):
        response = self.client.get('/apply/register/')
        self.assertEquals(response.status_code,200)

    def test_register_account_with_unconfirmed_email(self):
        """
        tests that error would be returned if email and confirmation
        email are different.
        """
        self.regis_data['email_confirmation'] = self.regis_data['email'] + 'xx'
        response = self.client.post('/apply/register/',self.regis_data)
        self.assertTemplateUsed(response,'application/registration.html')
        form = response.context['form']
        self.assertEquals(len(form._errors['email_confirmation']),1)


    def test_register_account(self):
        """
        tests that, when a user registers a new account, new Applicant
        is created, correct template is rendered after correct
        registration data is entered, and an email is sent.
        """
        org_email_setting = settings.FAKE_SENDING_EMAIL
        settings.FAKE_SENDING_EMAIL = False

        response = self.client.post('/apply/register/',
                                    self.regis_data)

        self.assertTemplateUsed(response,
                                'application/registration-success.html')

        apps = Applicant.objects.filter(email=self.regis_data['email']).all()
        self.assertEquals(len(apps),1)
        applicant = apps[0]
        self.assertEquals(applicant.first_name,self.regis_data['first_name'])
        self.assertEquals(applicant.email,self.regis_data['email'])

        self.assertEquals(len(mail.outbox),1)
        self.assertEquals(mail.outbox[0].to[0],self.regis_data['email'])
        settings.FAKE_SENDING_EMAIL = org_email_setting


    def create_user_and_get_password(self):
        org_email_setting = settings.FAKE_SENDING_EMAIL
        settings.FAKE_SENDING_EMAIL = False

        response = self.client.post('/apply/register/',
                                    self.regis_data)

        self.assertTemplateUsed(response,
                                'application/registration-success.html')

        self.assertEquals(len(mail.outbox),1)
        body = mail.outbox[0].body

        import re

        m = re.search('Your password is: (\w+)',body,re.M)
        password = m.group(1)

        return password


    def test_user_can_login_from_sent_password(self):
        """
        tests that, when a user registers a new account, an email is
        sent with a password, and that password can be used to login.
        """
        password = self.create_user_and_get_password()

        response = self.client.post('/apply/login/',
                                    {'email': self.regis_data['email'],
                                     'password': password})
        
        self.assertRedirects(response,'/apply/personal/')


    def test_user_cannot_register_again_after_logged_in(self):
        """
        tests that, when a user registers a new account and logged in,
        that user cannot register again.
        """

        # create user
        password = self.create_user_and_get_password()

        # log in
        response = self.client.post('/apply/login/',
                                    {'email': self.regis_data['email'],
                                     'password': password})

        self.assertRedirects(response,'/apply/personal/')

        # register again
        response = self.client.post('/apply/register/',
                                    self.regis_data)

        self.assertTemplateUsed(response,'application/registration.html')
        form = response.context['form']
        self.assertEquals(len(form.non_field_errors()),1)
