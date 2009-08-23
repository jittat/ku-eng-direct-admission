# -*- coding: utf-8 -*-

from django.db import models

class Applicant(models.Model):
    first_name = models.CharField(max_length=200,
                                  verbose_name="ชื่อ")
    last_name = models.CharField(max_length=300,
                                 verbose_name="นามสกุล")
    national_id = models.CharField(max_length=20)
    birth_date = models.DateField(verbose_name="วันเกิด")
    nationality = models.CharField(max_length=50,
                                   verbose_name="สัญชาติ")
    ethnicity = models.CharField(max_length=50,
                                 verbose_name="เชื้อชาติ")
    email = models.EmailField()





