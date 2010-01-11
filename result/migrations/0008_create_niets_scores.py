# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.result.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'NIETSScores'
        db.create_table('result_nietsscores', (
            ('id', orm['result.nietsscores:id']),
            ('applicant', orm['result.nietsscores:applicant']),
            ('score_list', orm['result.nietsscores:score_list']),
        ))
        db.send_create_signal('result', ['NIETSScores'])
        
        # Changing field 'AdmissionResult.applicant'
        # (to signature: django.db.models.fields.related.OneToOneField(unique=True, to=orm['application.Applicant']))
        db.alter_column('result_admissionresult', 'applicant_id', orm['result.admissionresult:applicant'])
        
        # Creating unique_together for [applicant] on AdmissionResult.
        db.create_unique('result_admissionresult', ['applicant_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [applicant] on AdmissionResult.
        db.delete_unique('result_admissionresult', ['applicant_id'])
        
        # Deleting model 'NIETSScores'
        db.delete_table('result_nietsscores')
        
        # Changing field 'AdmissionResult.applicant'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['application.Applicant']))
        db.alter_column('result_admissionresult', 'applicant_id', orm['result.admissionresult:applicant'])
        
    
    
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
        'application.major': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'result.admissionresult': {
            'additional_info': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'admitted_major': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Major']", 'null': 'True'}),
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'admission_result'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admitted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_waitlist': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'result.nietsscores': {
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'NIETS_scores'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score_list': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'result_set_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }
    
    complete_apps = ['result']
