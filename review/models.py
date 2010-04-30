# -*- coding: utf-8 -*-
from django.db import models

from application.fields import IntegerListField  
from application.models import Applicant

class ReviewField(models.Model):
    short_name = models.CharField(max_length=30,
                                  verbose_name="ชื่อสั้นภายใน")
    name = models.CharField(max_length=100,
                            verbose_name="ชื่อเอกสาร")
    order = models.IntegerField(
        verbose_name="ลำดับการเรียงเอกสาร")
    required = models.BooleanField(default=True,
                                   verbose_name="เป็นเอกสารที่ต้องยื่น?")
    enabled = models.BooleanField(default=True)

    applicant_note_help_text = models.TextField(blank=True,
                                                verbose_name="คำอธิบายตอนกรอก"
                                                "หมายเหตุสำหรับผู้สมัคร")
    admin_note_help_text = models.TextField(blank=True,
                                            verbose_name="คำอธิบายตอนกรอก"
                                            "หมายเหตุสำหรับใช้ภายใน")
    applicant_note_format = models.CharField(max_length=200, 
                                             blank=True,
                                             verbose_name="รูปแบบสำหรับกรอก"
                                             "ของหมายเหตุสำหรับผู้สมัคร")
    admin_note_format = models.CharField(max_length=200, 
                                         blank=True,
                                         verbose_name=
                                         "รูปแบบสำหรับตรวจสอบ"
                                         "ของหมายเหตุภายใน")

    fields_cache = None

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']

    @staticmethod
    def build_fields_cache():
        fields = ReviewField.objects.all()
        fields_cache = {}
        fields_cache['id'] = {}
        fields_cache['short_name'] = {}
        fields_cache['raw'] = fields
        for f in fields:
            fields_cache['id'][f.id] = f
            fields_cache['short_name'][f.short_name] = f
        ReviewField.fields_cache = fields_cache

    @staticmethod
    def get_all_fields():
        if ReviewField.fields_cache==None:
            ReviewField.build_fields_cache()
            
        return fields_cache['raw']

    @staticmethod
    def get_field_by_short_name(name):
        if ReviewField.fields_cache==None:
            ReviewField.build_fields_cache()

        try:
            return ReviewField.fields_cache['short_name'][name]
        except:
            return None

    @staticmethod
    def get_field_by_id(id):
        if ReviewField.fields_cache==None:
            ReviewField.build_fields_cache()

        try:
            return ReviewField.fields_cache['id'][id]
        except:
            return None
        

class ReviewFieldResult(models.Model):
    applicant = models.ForeignKey(Applicant)
    review_field = models.ForeignKey(ReviewField)

    is_passed = models.NullBooleanField()
    applicant_note = models.CharField(blank=True, max_length=200)
    internal_note = models.CharField(blank=True, max_length=200)

    def __unicode__(self):
        return str(self.is_passed)

    @staticmethod
    def build_ref_to_review_field(results):
        for res in results:
            res.review_field = ReviewField.get_field_by_id(res.review_field_id)

    @staticmethod
    def get_applicant_review_results(applicant):
        results = ReviewFieldResult.objects.filter(applicant=applicant).all()
        ReviewFieldResult.build_ref_to_review_field(results)
        return results

    @staticmethod
    def get_applicant_review_error_results(applicant):
        results = (ReviewFieldResult.objects
                   .filter(applicant=applicant)
                   .filter(is_passed=False).all())
        ReviewFieldResult.build_ref_to_review_field(results)
        return results

    @staticmethod
    def is_field_with_error_result(applicant, field_name):
        results = ReviewFieldResult.get_applicant_review_error_results(applicant)
        for r in results:
            if r.review_field.short_name == field_name:
                return True
        return False


class CompletedReviewField(models.Model):
    national_id = models.CharField(max_length=20)
    review_field = models.ForeignKey(ReviewField)

    @staticmethod
    def get_for_applicant(applicant):
        national_id = applicant.personal_info.national_id
        completed_review_fields = (CompletedReviewField.objects
                                   .filter(national_id=national_id)
                                   .select_related(depth=1))
        return [cr.review_field for cr in completed_review_fields]

