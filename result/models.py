# -*- coding: utf-8 -*-
from django.db import models

from application.fields import IntegerListField
from application.models import Applicant

class ReportCategory(models.Model):
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
    def get_category_by_name(name):
        if ReportCategory._categories==None:
            cat = {}
            for category in ReportCategory.objects.all():
                cat[category.name] = category
            ReportCategory._categories = cat
        return ReportCategory._categories[name]

    @staticmethod
    def get_category_by_app_first_name(first_name):
        return ReportCategory.get_category_by_name(
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
