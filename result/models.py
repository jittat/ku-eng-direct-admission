# -*- coding: utf-8 -*-
from django.db import models

from application.fields import IntegerListField
from application.models import Applicant, Major

class ReportCategory(models.Model):
    result_set_id = models.IntegerField(null=True)
    name = models.CharField(max_length=5)
    order = models.IntegerField()

    _categories = None

    @staticmethod
    def is_cons(c):
        u"""
        >>> ReportCategory.is_cons(u'ก')
        True
        >>> ReportCategory.is_cons(u'ฮ')
        True
        >>> ReportCategory.is_cons(u'เ')
        False
        >>> ReportCategory.is_cons(u'แ')
        False
        """
        return (c >= u'ก') and (c <= u'ฮ')

    @staticmethod
    def get_category_name_from_first_name(first_name):
        u"""
        >>> ReportCategory.get_category_name_from_first_name('John')
        'J'
        >>> ReportCategory.get_category_name_from_first_name('john')
        'J'

        >>> print ReportCategory.get_category_name_from_first_name(u'สมชาย')
        ส
        >>> print ReportCategory.get_category_name_from_first_name(u'เกียรติ')
        ก
        >>> print ReportCategory.get_category_name_from_first_name(u'ใจดี')
        จ
        """
        if (((first_name[0] >= u'a') and (first_name[0] <= u'z')) or
            ((first_name[0] >= u'A') and (first_name[0] <= u'Z'))): # roman?
            return first_name[0].upper()
        
        for c in first_name:
            if ReportCategory.is_cons(c):
                return c
        
        return ''

    @staticmethod
    def get_category_by_name(result_set_id, name):
        if ReportCategory._categories==None:
            cat = {}
            for category in ReportCategory.objects.all():
                cat[(category.result_set_id, category.name)] = category
            ReportCategory._categories = cat
        return ReportCategory._categories[(result_set_id, name)]

    @staticmethod
    def get_category_by_app_first_name(result_set_id, first_name):
        return ReportCategory.get_category_by_name(
            result_set_id,
            ReportCategory.get_category_name_from_first_name(
                first_name))

    class Meta:
        ordering = ['order']


class QualifiedApplicant(models.Model):
    ticket_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=300)

    order = models.IntegerField()

    category = models.ForeignKey(ReportCategory)

    applicant = models.ForeignKey(Applicant)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s %s %s' % (
            self.ticket_number,
            self.first_name,
            self.last_name)

class AdmissionResult(models.Model):
    applicant = models.OneToOneField(Applicant, 
                                     related_name='admission_result')
    
    is_admitted = models.BooleanField()
    is_waitlist = models.BooleanField()
    
    admitted_major = models.ForeignKey(Major, null=True)

    additional_info = models.TextField(null=True)


class NIETSScores(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name='NIETS_scores')
    score_list = models.CharField(max_length=200)

    def as_list(self):
        if self.score_list!='':
            return [float(s) for s in self.score_list.split(',')]
        else:
            return None

    def as_list_by_exam_round(self):
        if self.score_list=='':
            return None
        else:
            l = self.as_list()
            out = []
            while len(l)!=0:
                out.append(l[:3])
                l = l[3:]
            return out
