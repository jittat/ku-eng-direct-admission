# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.result.models import *

class Migration:

    no_dry_run = True

    def forwards(self, orm):
        for cat in orm.ReportCategory.objects.all():
            cat.result_set_id = 1
            cat.save()
    
    def backwards(self, orm):
        "Write your backwards migration here"
    
    
    models = {
        'application.applicant': {
            'activation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'doc_submission_method': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'has_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_related_model': ('IntegerListField', [], {'default': 'None'}),
            'hashed_password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_offline': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'result.qualifiedapplicant': {
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Applicant']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['result.ReportCategory']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'result_set_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'ticket_number': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'result.reportcategory': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'result_set_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }
    
    complete_apps = ['result']
