# -*- coding: utf-8 -*-
import re
import datetime

from django import forms

from application.models import Applicant, PersonalInfo
from application.models import Address, ApplicantAddress, Education, Major
from widgets import ThaiSelectDateWidget
from commons.local import APP_TITLE_FORM_CHOICES
from commons.utils import validate_national_id, validate_phone_number
from django.forms.util import ErrorList

class LoginForm(forms.Form):
    #email = forms.EmailField()
    #application_id = forms.CharField(required=False)
    national_id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def uses_email(self):
        return False


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        applicants = (Applicant.objects
                      .filter(email=email))
        if len(applicants)==1:
            applicant = applicants[0]
            return {'email': email,
                    'applicant': applicant}
        else:
            raise forms.ValidationError(u'ไม่มีผู้ใช้ที่ใช้อีเมล์: ' +
                                        email)

class StatusRequestForm(forms.Form):
    email = forms.EmailField()


class RegistrationForm(forms.Form):
    title = forms.ChoiceField(choices=APP_TITLE_FORM_CHOICES)
    first_name = forms.CharField(label=u'ชื่อ')
    last_name = forms.CharField(label=u'นามสกุล')
    email = forms.EmailField(label=u'อีเมล์')
    email_confirmation = forms.EmailField(label=u'ยืนยันอีเมล์')
    national_id = forms.CharField(label=u'รหัสประจำตัวประชาชน')
    national_id_confirmation = forms.CharField(label=u'ยืนยันรหัสประจำตัวประชาชน')

    def check_confirmation(self, field_name, field_name_confirmation, error_message):
        f = self.cleaned_data.get(field_name)
        f_confirmation = self.cleaned_data.get(field_name_confirmation)

        if f and f_confirmation and (
            f != f_confirmation):

            self._errors[field_name_confirmation] = ErrorList(
                [error_message])
            del self.cleaned_data[field_name]
            del self.cleaned_data[field_name_confirmation]

    def clean(self):
        cleaned_data = self.cleaned_data
        self.check_confirmation('email', 'email_confirmation',
                           u'อีเมล์ที่ยืนยันไม่ตรงกัน')
        self.check_confirmation('national_id', 'national_id_confirmation',
                           u'รหัสประจำตัวประชาชนที่ยืนยันไม่ตรงกัน')
        return cleaned_data

    def clean_national_id(self):
        nat = self.cleaned_data['national_id']
        
        if not validate_national_id(nat):
            raise forms.ValidationError(u'รหัสประชาชนที่ป้อนไม่ถูกต้อง')
        return nat


    def get_applicant(self):
        return Applicant(title=self.cleaned_data['title'],
                         first_name=self.cleaned_data['first_name'],
                         last_name=self.cleaned_data['last_name'],
                         email=self.cleaned_data['email'],
                         national_id=self.cleaned_data['national_id'])


class ActivationNameForm(forms.Form):
    title = forms.ChoiceField(choices=APP_TITLE_FORM_CHOICES)
    first_name = forms.CharField(label=u'ชื่อ')
    last_name = forms.CharField(label=u'นามสกุล')


THIS_YEAR = datetime.date.today().year
APPLICANT_BIRTH_YEARS = range(THIS_YEAR-30,THIS_YEAR-10)

class PersonalInfoForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=ThaiSelectDateWidget(years=APPLICANT_BIRTH_YEARS),
        label=u"วันเกิด")

    def clean_national_id(self):
        if re.match(r'^(\d){13}$',self.cleaned_data['national_id']) == None:
            raise forms.ValidationError("รหัสประจำตัวประชาชนไม่ถูกต้อง")
        return self.cleaned_data['national_id']

    def clean_phone_number(self):
        if not validate_phone_number(self.cleaned_data['phone_number']):
            raise forms.ValidationError("หมายเลขโทรศัพท์ไม่ถูกต้อง")
        return self.cleaned_data['phone_number']

    class Meta:
        model = PersonalInfo
        exclude = ['applicant']


class AddressForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(
            attrs={'size':6}))

    village_number = forms.IntegerField(required=False,
            widget=forms.TextInput(
            attrs={'size':6}))

    def clean_postal_code(self):
        if re.match(r'^(\d){5}$',self.cleaned_data['postal_code']) == None:
            raise forms.ValidationError("รหัสไปรษณีย์ไม่ถูกต้อง")
        return self.cleaned_data['postal_code']        

    def clean_phone_number(self):
        if not validate_phone_number(self.cleaned_data['phone_number']):
            raise forms.ValidationError("หมายเลขโทรศัพท์ไม่ถูกต้อง")
        return self.cleaned_data['phone_number']

    class Meta:
        model = Address


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['applicant']


class SingleMajorPreferenceForm(forms.Form):
    major = forms.ModelChoiceField(queryset=Major.objects.all(),
                                   label='สาขาวิชา',
                                   empty_label='ยังไม่ได้เลือก')
