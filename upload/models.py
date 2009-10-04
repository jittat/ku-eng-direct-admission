# _*_  coding: utf-8 _*_

import os

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from application.models import Applicant

uploaded_storage = FileSystemStorage(location=settings.UPLOADED_DOC_PATH)

def get_doc_path(applicant, filename):
    return ('doc/%d/%s' % (applicant.id, filename))

def get_doc_fullpath(applicant, filename):
    return os.path.join(settings.UPLOADED_DOC_PATH,
                        get_doc_path(applicant, filename))

def get_field_filename(org_filename, field_name):
    first, ext = os.path.splitext(org_filename)    
    return field_name + ext

def get_field_thumbnail_filename(field_name):
    return field_name + '.thumbnail.png'

def get_doc_path_function(field_name):
    "returns a function for modifying uploaded filename"
    def f(instance, filename):
        field_filename = get_field_filename(filename, field_name)
        return get_doc_path(instance.applicant, field_filename)
    return f


class AppDocs(models.Model):
    applicant = models.OneToOneField(Applicant)
    picture = models.ImageField(
        upload_to=get_doc_path_function('picture'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='รูปถ่าย')
    edu_certificate = models.ImageField(
        upload_to=get_doc_path_function('edu_certificate'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='ใบรับรองการศึกษา')

    abroad_edu_certificate = models.ImageField(
        upload_to=get_doc_path_function('abroad_edu_certificate'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='หลักฐานการศึกษาต่างประเทศ')

    gat_score = models.ImageField(
        upload_to=get_doc_path_function('gat_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน GAT')

    pat1_score = models.ImageField(
        upload_to=get_doc_path_function('pat1_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน PAT1')

    pat3_score = models.ImageField(
        upload_to=get_doc_path_function('pat3_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน PAT3')

    anet_score = models.ImageField(
        upload_to=get_doc_path_function('anet_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน A-NET ความถนัดทางวิศวกรรม')

    nat_id = models.ImageField(
        upload_to=get_doc_path_function('nat_id'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='สำเนาบัตรประจำตัวประชาชน หรือสำเนาบัตรนักเรียน')

    app_fee_doc = models.ImageField(
        upload_to=get_doc_path_function('app_fee_doc'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='หลักฐานใบนำฝากเงินค่าสมัคร')

    def thumbnail_path(self, field_name):
        return get_doc_fullpath(self.applicant, 
                                get_field_thumbnail_filename(field_name))

    @staticmethod
    def valid_field_name(field_name):
        return field_name in AppDocs.FormMeta.upload_fields    

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

