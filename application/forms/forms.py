# -*- coding: utf-8 -*-
import re
import datetime

from django import forms

from application.models import Applicant, PersonalInfo
from application.models import Address, ApplicantAddress, Education
from widgets import ThaiSelectDateWidget
from commons.local import APP_TITLE_FORM_CHOICES
from django.forms.util import ErrorList

def validate_phone_number(phone_number):
    return re.match(u'^([0-9\\- #]|ต่อ|ext)+$', phone_number) != None

class LoginForm(forms.Form):
    email = forms.EmailField()
    application_id = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'email' not in cleaned_data:
            return cleaned_data
        email = cleaned_data.get('email')
        application_id = cleaned_data.get('application_id')

        if email!='' and application_id=='':
            return cleaned_data

        if email!='' and application_id!='':  # use two identity
            del cleaned_data['email']
            del cleaned_data['application_id']
            self._errors['application_id'] = ErrorList(
                ['ไม่สามารถป้อนทั้งอีเมล์และหมายเลขพร้อมกัน'])
            return cleaned_data

        import re
        if not re.match(r'53[123]\d{5}', application_id):
            self._errors['application_id'] = ErrorList(
                ['หมายเลขประจำตัวไม่ถูกต้อง'])
            del cleaned_data['application_id']

        return cleaned_data

    def uses_email(self):
        return True
        cleaned_data = self.cleaned_data
        if 'email' not in cleaned_data:
            return False
        return self.cleaned_data['email'] != ''


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

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        email_confirmation = cleaned_data.get('email_confirmation')

        if email and email_confirmation and (
            email != email_confirmation): 

            self._errors['email_confirmation'] = ErrorList(
                ['อีเมล์ที่ยืนยันไม่ตรงกัน'])
            del cleaned_data['email']
            del cleaned_data['email_confirmation']

        return cleaned_data

    def get_applicant(self):
        return Applicant(title=self.cleaned_data['title'],
                         first_name=self.cleaned_data['first_name'],
                         last_name=self.cleaned_data['last_name'],
                         email=self.cleaned_data['email'])


class ActivationNameForm(forms.Form):
    title = forms.ChoiceField(choices=APP_TITLE_FORM_CHOICES)
    first_name = forms.CharField(label=u'ชื่อ')
    last_name = forms.CharField(label=u'นามสกุล')


THIS_YEAR = datetime.date.today().year
APPLICANT_BIRTH_YEARS = range(THIS_YEAR-30,THIS_YEAR-10)

class PersonalInfoForm(forms.ModelForm):
    national_id = forms.CharField(max_length=13,
                                  label=u"รหัสประจำตัวประชาชน")
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
    # TODO: add form validation

    def clean_gpax(self):
        gpax = self.cleaned_data['gpax']
        if gpax < 0 or gpax > 4:
            raise forms.ValidationError("เกรดเฉลี่ยไม่ถูกต้อง")
        return self.cleaned_data['gpax']

    def validate_score_in_range(self, name, display_name, 
                                score_min, score_max):
        score = self.cleaned_data[name]
        if (score == None) or (score < score_min) or (score > score_max):
            raise forms.ValidationError("คะแนน %s ไม่ถูกต้อง" % (display_name,))
        return score

    def clean_gat(self):
        if not self.cleaned_data['uses_gat_score']:
            return self.cleaned_data['gat']
        return self.validate_score_in_range('gat', 'GAT', 0, 300)

    def clean_pat1(self):
        if not self.cleaned_data['uses_gat_score']:
            return self.cleaned_data['pat1']
        return self.validate_score_in_range('pat1', 'PAT1', 0, 300)

    def clean_pat3(self):
        if not self.cleaned_data['uses_gat_score']:
            return self.cleaned_data['pat3']
        return self.validate_score_in_range('pat3', 'PAT3', 0, 300)

    def clean_anet(self):
        if self.cleaned_data['uses_gat_score']:
            return self.cleaned_data['anet']

        if self.cleaned_data['anet'] < 35:
            for s in ['gat','pat1','pat3']:
                sc = self.cleaned_data[s]
                if (sc==None) or (sc < 0) or (sc > 300):
                    raise forms.ValidationError("คะแนน A-NET น้อยกว่า 35 ให้ป้อนคะแนน GAT/PAT เพื่อพิจารณาด้วย")
        return self.validate_score_in_range('anet', 'A-NET', 0, 100)

    class Meta:
        model = Education
        exclude = ['applicant']

