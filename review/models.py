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

    field_cache = None

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']

    @staticmethod
    def get_all_fields():
        if ReviewField.field_cache==None:
            fields = ReviewField.objects.all()
            d = {}
            for f in fields:
                d[f.short_name] = f
            ReviewField.field_cache = d

        return ReviewField.field_cache


class ReviewFieldResult(models.Model):
    applicant = models.ForeignKey(Applicant)
    review_field = models.ForeignKey(ReviewField)

    is_passed = models.NullBooleanField()
    applicant_note = models.CharField(max_length=200)
    internal_note = models.CharField(max_length=200)

    def __unicode__(self):
        return is_passed


