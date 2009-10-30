# -*- coding: utf-8 -*-
import re
import datetime

from django import forms

from application.models import Applicant
from application.models import Address, ApplicantAddress, Education
from widgets import ThaiSelectDateWidget

def validate_phone_number(phone_number):
    # TODO: describe ext format in web form
    return re.match(u'^([0-9\\- #]|ต่อ|ext)+$', phone_number) != None

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        applicants = (Applicant.objects
                      .filter(email=email))
        print applicants
        if len(applicants)==1:
            applicant = applicants[0]
            return {'email': email,
                    'applicant': applicant}
        else:
            raise forms.ValidationError(u'ไม่มีผู้ใช้ที่ใช้อีเมล์: ' +
                                        email)
        

class RegistrationForm(forms.ModelForm):
    email_confirmation = forms.EmailField()

    def clean_email_confirmation(self):
        if (self.cleaned_data['email'] !=
            self.cleaned_data['email_confirmation']):
            raise forms.ValidationError("อีเมล์ที่ระบุไม่ตรงกัน")
        return self.cleaned_data['email_confirmation']

    class Meta:
        model = Applicant
        exclude = ('hashed_password', 
                   'is_submitted',
                   'doc_submission_method')


THIS_YEAR = datetime.date.today().year
APPLICANT_BIRTH_YEARS = range(THIS_YEAR-30,THIS_YEAR-10)

class ApplicantCoreForm(forms.ModelForm):
    email_confirmation = forms.EmailField()
    birth_date = forms.DateField(
        widget=ThaiSelectDateWidget(years=APPLICANT_BIRTH_YEARS))

    def clean_national_id(self):
        if re.match(r'^(\d){13}$',self.cleaned_data['national_id']) == None:
            raise forms.ValidationError("รหัสประจำตัวประชาชนไม่ถูกต้อง")
        return self.cleaned_data['national_id']

    def clean_phone_number(self):
        if not validate_phone_number(self.cleaned_data['phone_number']):
            raise forms.ValidationError("หมายเลขโทรศัพท์ไม่ถูกต้อง")
        return self.cleaned_data['phone_number']

    class Meta:
        model = Applicant


class AddressForm(forms.ModelForm):
    # TODO: add form validation
    class Meta:
        model = Address


class EducationForm(forms.ModelForm):
    # TODO: add form validation
    class Meta:
        model = Education
        exclude = ['applicant']

