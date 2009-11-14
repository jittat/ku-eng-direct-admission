# -*- coding: utf-8 -*-

from application.models import Applicant, Registration

class ApplicantPreparation():

    REGIS_DATA = {
        'title': u'นาย',
        'first_name': u'สมชาย',
        'last_name': u'ใจดี',
        #'first_name': 'somchai',
        #'last_name': 'jaidee',
        'email': 'somchai@gmail.com',
        }

    def __init__(self, regis_data=None):
        if regis_data==None:
            self.regis_data = dict(ApplicantPreparation.REGIS_DATA)
        else:
            self.regis_data = dict(regis_data)
    
    def create_applicant(self):
        applicant = Applicant(
            title=self.regis_data['title'],
            first_name=self.regis_data['first_name'],
            last_name=self.regis_data['last_name'],
            email=self.regis_data['email']
            )
        password = applicant.random_password()
        applicant.save()
        registration = Registration(
            applicant=applicant,
            first_name=applicant.first_name,
            last_name=applicant.last_name
            )
        registration.random_activation_key()
        registration.save()

        return applicant, password
