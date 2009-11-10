# -*- coding: utf-8 -*-
import re
import datetime

from django import forms

from application.models import Applicant, PersonalInfo
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
        if len(applicants)==1:
            applicant = applicants[0]
            return {'email': email,
                    'applicant': applicant}
        else:
            raise forms.ValidationError(u'ไม่มีผู้ใช้ที่ใช้อีเมล์: ' +
                                        email)

class RegistrationForm(forms.Form):
    first_name = forms.CharField(label=u'ชื่อ')
    last_name = forms.CharField(label=u'นามสกุล')
    email = forms.EmailField(label=u'อีเมล์')
    email_confirmation = forms.EmailField(label=u'ยืนยันอีเมล์')

    def clean_email_confirmation(self):
        if (self.cleaned_data['email'] !=
            self.cleaned_data['email_confirmation']):
            raise forms.ValidationError("อีเมล์ที่ระบุไม่ตรงกัน")
        return self.cleaned_data['email_confirmation']

    def get_applicant(self):
        return Applicant(first_name=self.cleaned_data['first_name'],
                         last_name=self.cleaned_data['last_name'],
                         email=self.cleaned_data['email'])


class ActivationNameForm(forms.Form):
    first_name = forms.CharField(label=u'ชื่อ')
    last_name = forms.CharField(label=u'นามสกุล')


THIS_YEAR = datetime.date.today().year
APPLICANT_BIRTH_YEARS = range(THIS_YEAR-30,THIS_YEAR-10)

class PersonalInfoForm(forms.ModelForm):
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
        model = PersonalInfo
        exclude = ['applicant']


class AddressForm(forms.ModelForm):
    # TODO: add form validation
    class Meta:
        model = Address


class EducationForm(forms.ModelForm):
    # TODO: add form validation

    def clean_gpax(self):
        gpax = self.cleaned_data['gpax']
        if gpax < 0 or gpax > 4:
            raise forms.ValidationError("เกรดเฉลี่ยไม่ถูกต้อง")
        return self.cleaned_data['gpax']

    def clean_gat(self):
        gat = self.cleaned_data['gat']
        if gat < 0 or gat > 300:
            raise forms.ValidationError("คะแนน GAT ไม่ถูกต้อง")
        return self.cleaned_data['gat']

    def clean_pat1(self):
        pat1 = self.cleaned_data['pat1']
        if pat1 < 0 or pat1 > 300:
            raise forms.ValidationError("คะแนน PAT1 ไม่ถูกต้อง")
        return self.cleaned_data['pat1']

    def clean_pat3(self):
        pat3 = self.cleaned_data['pat3']
        if pat3 < 0 or pat3 > 300:
            raise forms.ValidationError("คะแนน PAT3 ไม่ถูกต้อง")
        return self.cleaned_data['pat3']

    class Meta:
        model = Education
        exclude = ['applicant']

