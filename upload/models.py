# _*_  coding: utf-8 _*_

import os

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from application.models import Applicant

uploaded_storage = FileSystemStorage(location=settings.UPLOADED_DOC_PATH)

def get_doc_path(instance, filename, new_filename):
    first, ext = os.path.splitext(filename)    
    return ('doc/%d/%s%s' % (instance.applicant.id, new_filename, ext))

def get_doc_path_for(new_filename):
    "returns a function for modifying uploaded filename"
    def f(instance, filename):
        return get_doc_path(instance, filename, new_filename)
    return f


class AppDocs(models.Model):
    applicant = models.OneToOneField(Applicant)
    picture = models.ImageField(
        upload_to=get_doc_path_for('picture'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='รูปถ่าย')
    edu_certificate = models.ImageField(
        upload_to=get_doc_path_for('edu_certificate'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='ใบรับรองการศึกษา')

    abroad_edu_certificate = models.ImageField(
        upload_to=get_doc_path_for('abroad_edu_certificate'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='หลักฐานการศึกษาต่างประเทศ')

    gat_score = models.ImageField(
        upload_to=get_doc_path_for('gat_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน GAT')

    pat1_score = models.ImageField(
        upload_to=get_doc_path_for('pat1_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน PAT1')

    pat3_score = models.ImageField(
        upload_to=get_doc_path_for('pat3_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน PAT3')

    anet_score = models.ImageField(
        upload_to=get_doc_path_for('anet_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน A-NET ความถนัดทางวิศวกรรม')

    nat_id = models.ImageField(
        upload_to=get_doc_path_for('nat_id'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='สำเนาบัตรประจำตัวประชาชน หรือสำเนาบัตรนักเรียน')

    app_fee_doc = models.ImageField(
        upload_to=get_doc_path_for('app_fee_doc'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='หลักฐานใบนำฝากเงินค่าสมัคร')

    class FormMeta:
        upload_fields = [
            'picture', 
            'edu_certificate',
            'abroad_edu_certificate',
            'gat_score',
            'pat1_score',
            'pat3_score',
            'anet_score',
            'nat_id',
            'app_fee_doc']

