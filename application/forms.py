# -*- coding: utf-8 -*-
import re

from django import forms

from models import Applicant, ApplicantAccount
from models import Address, ApplicantAddress, Education

def validate_phone_number(phone_number):
    # TODO: describe ext format in web form
    return re.match(u'^([0-9\\- #]|ต่อ|ext)+$', phone_number) != None

class ApplicantCoreForm(forms.ModelForm):
    email_confirmation = forms.EmailField()

    def clean_national_id(self):
        if re.match(r'^(\d){13}$',self.cleaned_data['national_id']) == None:
            raise forms.ValidationError("รหัสประจำตัวประชาชนไม่ถูกต้อง")
        return self.cleaned_data['national_id']

    def clean_phone_number(self):
        if not validate_phone_number(self.cleaned_data['phone_number']):
            raise forms.ValidationError("หมายเลขโทรศัพท์ไม่ถูกต้อง")
        return self.cleaned_data['phone_number']

    def clean_email_confirmation(self):
        if (self.cleaned_data['email'] !=
            self.cleaned_data['email_confirmation']):
            raise forms.ValidationError("อีเมล์ที่ระบุไม่ตรงกัน")
        return self.cleaned_data['email_confirmation']

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

