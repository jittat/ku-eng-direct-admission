# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from application.fields import IntegerListField
from application.models import Applicant

class AdmissionMajorPreference(models.Model):
    applicant = models.ForeignKey(Applicant,
                                  related_name='admission_major_preferences')
    round_number = models.IntegerField(default=0)
    is_accepted_list = IntegerListField()

    ptype = models.IntegerField(default=0)

    class PrefType():
        PREF_NO_MOVE = 1
        PREF_MOVE_UP_INCLUSIVE = 2
        PREF_MOVE_UP_STRICT = 3
        PREF_WITHDRAWN = 4

        def __init__(self, ptype):
            self.ptype = ptype

        def is_no_move(self):
            return self.ptype == self.PREF_NO_MOVE
        
        def is_move_up_inclusive(self):
            return self.ptype == self.PREF_MOVE_UP_INCLUSIVE
        
        def is_move_up_strict(self):
            return self.ptype == self.PREF_MOVE_UP_STRICT
        
        def is_withdrawn(self):
            return self.ptype == self.PREF_WITHDRAWN

        @staticmethod
        def new_empty():
            return AdmissionMajorPreference.PrefType(0)

    PrefType.NO_MOVE = PrefType(PrefType.PREF_NO_MOVE)
    PrefType.MOVE_UP_INCLUSIVE = PrefType(PrefType.PREF_MOVE_UP_INCLUSIVE)
    PrefType.MOVE_UP_STRICT = PrefType(PrefType.PREF_MOVE_UP_STRICT)
    PrefType.WITHDRAWN = PrefType(PrefType.PREF_WITHDRAWN)

    preftype_dict = { 1: PrefType.NO_MOVE,
                      2: PrefType.MOVE_UP_INCLUSIVE,
                      3: PrefType.MOVE_UP_STRICT,
                      4: PrefType.WITHDRAWN }

    @staticmethod
    def new_for_applicant(applicant):
        pref = AdmissionMajorPreference()
        pref.applicant = applicant
        admission_result = applicant.get_latest_admission_result()
        if ((not admission_result) or
            (not admission_result.is_admitted)):
            pref.is_accepted_list = []
            return pref

        admitted_major = admission_result.admitted_major
        majors = applicant.preference.get_major_list()
        mcount = len(majors)
        alist = [0] * mcount
        i = 0
        while (i < mcount) and (majors[i].id != admitted_major.id):
            alist[i] = 1
            i += 1
        if i < mcount:   # for admitted major
            alist[i] = 1
        pref.is_accepted_list = alist
        return pref


    def is_applicant_admitted(self):
        applicant = self.applicant
        if not applicant:
            return False
        
        admission_result = applicant.get_latest_admission_result()
        return (admission_result) and (admission_result.is_admitted)


    def get_accepted_majors(self):
        if not self.is_applicant_admitted():
            return []
        majors = self.applicant.preference.get_major_list()
        accepted_majors = [m 
                           for a, m
                           in zip(self.is_accepted_list,
                                  majors)
                           if a]
        return accepted_majors


    def set_ptype_cache(self, save=True):
        if not self.is_applicant_admitted():
            self.ptype = 4

        else:
            accepted_majors = self.get_accepted_majors()
            assigned_majors = self.applicant.get_latest_admission_result().admitted_major

            if len(accepted_majors)==0:
                self.ptype = 4
            elif (len(accepted_majors)==1 and
                  accepted_majors[0].id == assigned_majors.id):
                self.ptype = 1
            elif assigned_majors.id in [a.id for a in accepted_majors]:
                self.ptype = 2
            else:
                self.ptype = 3

        if save:
            self.save()

    
    def get_pref_type(self):
        if self.ptype==0:
            self.set_ptype_cache()
        return AdmissionMajorPreference.preftype_dict[self.ptype]


    def get_display(self):
        pref_type = self.get_pref_type()
        if pref_type == AdmissionMajorPreference.PrefType.WITHDRAWN:
            return u'สละสิทธิ์'
        elif pref_type == AdmissionMajorPreference.PrefType.NO_MOVE:
            return u'ยืนยันสิทธิ์ในสาขาที่ได้รับคัดเลือก และไม่ต้องการเข้ารับการพิจารณาเลื่อนอันดับอีก'
        elif pref_type == AdmissionMajorPreference.PrefType.MOVE_UP_INCLUSIVE:
            return u'ยืนยันสิทธิ์ในสาขาที่ได้รับคัดเลือก และต้องการเข้ารับการพิจารณาเลื่อนอันดับในสาขาที่อยู่ในอันดับสูงกว่า'
        else:
            return u'ยืนยันสิทธิ์ในสาขาที่ได้รับคัดเลือก และต้องการเข้ารับการพิจารณาเลื่อนอันดับในสาขาที่อยู่ในอันดับสูงกว่า ถ้าไม่ได้รับการพิจารณาจะสละสิทธิ์ในสาขาที่ได้รับคัดเลือกนี้'


    def is_withdrawn(self):
        pref_type = self.get_pref_type()
        return pref_type == AdmissionMajorPreference.PrefType.WITHDRAWN


class AdmissionConfirmation(models.Model):
    applicant = models.ForeignKey(Applicant, 
                                  related_name='admission_confirmations')
    round_number = models.IntegerField(default=0)
    paid_amount = models.IntegerField(default=0)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-confirmed_at']

class Round2ApplicantConfirmation(models.Model):
    applicant = models.OneToOneField(Applicant, related_name='round2_confirmation')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(
        choices=((True,u'ยืนยัน'),
                 (False,u'สละสิทธิ์')),
        default=True,
        verbose_name=u'การยืนยันการขอรับพิจารณาคัดเลือก')
    is_applying_for_survey_engr = models.BooleanField(
        choices=((True,u'ต้องการ'),
                 (False,u'ไม่ต้องการ')),
        default=False,
        verbose_name=u'ถ้าไม่ได้คัดเลือกในสาขาที่สมัครในตอนแรก ต้องการให้พิจารณาคัดเลือกในสาขาวิศวกรรมสำรวจหรือไม่?')


# REST api
from django_restapi.resource import Resource
from django_restapi.authentication import HttpBasicAuthentication
from django.http import HttpResponse
import json

class AdmissionConfirmationResource(Resource):
    def __init__(self, authentication=None,
                 mimetype=None):
        Resource.__init__(self, authentication, ('GET',), mimetype)

    def read(self, request, *args, **kwargs):
        confirmation = AdmissionConfirmation.objects.all().select_related(depth=1)
        results = []
        for c in confirmation:
            result = {'national_id': c.applicant.personal_info.national_id}
            results.append(result)
        return HttpResponse(json.dumps(results))

confirmation_resource = AdmissionConfirmationResource(
    authentication = HttpBasicAuthentication()
)

