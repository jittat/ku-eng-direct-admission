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
    picture = models.ImageField(upload_to=get_doc_path_for('picture'),
                                storage=uploaded_storage,
                                blank=True,
                                verbose_name='รูปถ่าย')
    edu_certificate = models.ImageField(
        upload_to=get_doc_path_for('edu_certificate'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='ใบรับรองการศึกษา')

    class FormMeta:
        upload_fields = ['picture', 'edu_certificate']

