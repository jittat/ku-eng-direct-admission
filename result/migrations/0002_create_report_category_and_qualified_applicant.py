# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.result.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ReportCategory'
        db.create_table('result_reportcategory', (
            ('id', orm['result.reportcategory:id']),
            ('name', orm['result.reportcategory:name']),
            ('order', orm['result.reportcategory:order']),
        ))
        db.send_create_signal('result', ['ReportCategory'])
        
        # Adding model 'QualifiedApplicant'
        db.create_table('result_qualifiedapplicant', (
            ('id', orm['result.qualifiedapplicant:id']),
            ('ticket_number', orm['result.qualifiedapplicant:ticket_number']),
            ('first_name', orm['result.qualifiedapplicant:first_name']),
            ('last_name', orm['result.qualifiedapplicant:last_name']),
            ('order', orm['result.qualifiedapplicant:order']),
            ('category', orm['result.qualifiedapplicant:category']),
            ('applicant', orm['result.qualifiedapplicant:applicant']),
        ))
        db.send_create_signal('result', ['QualifiedApplicant'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ReportCategory'
        db.delete_table('result_reportcategory')
        
        # Deleting model 'QualifiedApplicant'
        db.delete_table('result_qualifiedapplicant')
        
    
    
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
            'ticket_number': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'result.reportcategory': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        }
    }
    
    complete_apps = ['result']
