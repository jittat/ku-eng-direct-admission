# -*- coding: utf-8 -*-
import re
import datetime

from django import forms

from application.models import Applicant, PersonalInfo
from application.models import Address, ApplicantAddress, Education, Major
from widgets import ThaiSelectDateWidget
from commons.local import APP_TITLE_FORM_CHOICES
from django.forms.util import ErrorList

def validate_phone_number(phone_number):
    return re.match(u'^([0-9\\- #]|ต่อ|ext)+$', phone_number) != None

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
                         email=self.cleaned_data['email'],
                         national_id=self.cleaned_data['national_id'])


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
        try:
            score = self.cleaned_data[name]
        except:
            raise forms.ValidationError("คะแนน %s ไม่ถูกต้อง" % (display_name,))
        if (score == None) or (score < score_min) or (score > score_max):
            raise forms.ValidationError("คะแนน %s ไม่ถูกต้อง" % (display_name,))
        return score

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['uses_gat_score']:
            self.validate_score_in_range('gat', 'GAT', 0, 300)
            self.validate_score_in_range('pat1', 'PAT1', 0, 300)
            self.validate_score_in_range('pat3', 'PAT3', 0, 300)
        else:
            self.validate_score_in_range('anet', 'A-NET', 0, 100)
            if cleaned_data['anet'] < 35:
                sc = self.cleaned_data['anet_total_score']
                if sc==None:
                    raise forms.ValidationError("คะแนน A-NET น้อยกว่า 35 ให้ป้อนคะแนนรวมเพื่อพิจารณาด้วย")
                elif sc < 5000:
                    raise forms.ValidationError("คะแนน A-NET น้อยกว่า 35 จะต้องมีคะแนนรวมอย่างน้อย 5000")
        return cleaned_data

    class Meta:
        model = Education
        exclude = ['applicant']


class SingleMajorPreferenceForm(forms.Form):
    major = forms.ModelChoiceField(queryset=Major.objects.all(),
                                   label='สาขาวิชา',
                                   empty_label='ยังไม่ได้เลือก')
