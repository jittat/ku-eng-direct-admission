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

    is_final_admitted = models.BooleanField(default=False)
    final_admitted_major = models.ForeignKey(Major, null=True, 
                                             related_name='final_results')

    @staticmethod
    def new_for_applicant(applicant):
        res = AdmissionResult(applicant=applicant,
                              is_admitted=False,
                              is_waitlist=False,
                              is_final_admitted=False)
        return res

class ScoreStat:

    SUPER_ZMAX = 8

    def __init__(self, mean, sd, max_score):
        self.mean = mean
        self.sd = sd
        self.max_score = max_score

    def cal_score(self, x):
        z = (x - self.mean) / self.sd
        return 0.5 + 0.5 * z / ScoreStat.SUPER_ZMAX

SCORE_STATS = [
    { 'gat': ScoreStat(78.09, 44.32, 290),
      'pat1': ScoreStat(88.33, 30.63, 300),
      'pat3': ScoreStat(108.66, 26.17, 240) },
    { 'gat': ScoreStat(93.10, 51.13, 287.5),
      'pat1': ScoreStat(87.11, 31.14, 300),
      'pat3': ScoreStat(97.86, 28.56, 260) },
    { 'gat': ScoreStat(106.78, 55.59, 292.5),
      'pat1': ScoreStat(63.56, 25.90, 270),
      'pat3': ScoreStat(86.73, 24.64, 237) }
    ]
EXAM_COUNT = len(SCORE_STATS)


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

    
    @staticmethod
    def extract_gatpat_scores(score_list):
        scores = {'gat': [0] * EXAM_COUNT,
                  'pat1': [0] * EXAM_COUNT,
                  'pat3': [0] * EXAM_COUNT}

        i = 0
        for e in range(EXAM_COUNT):
            for exam in ['gat','pat1','pat3']:
                scores[exam][e] = score_list[i]
                i += 1

        return scores

    def get_best_normalized_score(self, test_name):
        all_scores = self.as_list()
        scores = NIETSScores.extract_gatpat_scores(all_scores)
        best_score = 0
        raw_score = 0
        for i in range(EXAM_COUNT):
            x = scores[test_name][i]
            score = SCORE_STATS[i][test_name].cal_score(x)
            if score > best_score:
                best_score = score
                raw_score = x
        return best_score, raw_score

    def get_score(self, gpax=None):
        gat, gs = self.get_best_normalized_score('gat')
        pat1, p1s = self.get_best_normalized_score('pat1')
        pat3, p3s = self.get_best_normalized_score('pat3')
        if gpax==None:
            gpax = self.applicant.education.gpax
        score = ((gpax/4.0*0.1) + 
                 gat * 0.2 +
                 pat1 * 0.2 + 
                 pat3 * 0.5)
        return 10000.0 * score

    def get_best_test_scores(self):
        gat, gs = self.get_best_normalized_score('gat')
        pat1, p1s = self.get_best_normalized_score('pat1')
        pat3, p3s = self.get_best_normalized_score('pat3')
        return [gs, p1s, p3s]

