# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.application.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'SubmissionInfo.doc_reviewed_at'
        db.add_column('application_submissioninfo', 'doc_reviewed_at', orm['application.submissioninfo:doc_reviewed_at'])
        db.create_index('application_submissioninfo',['doc_reviewed_at'])
    
    
    def backwards(self, orm):
        
        # Deleting field 'SubmissionInfo.doc_reviewed_at'
        db.delete_column('application_submissioninfo', 'doc_reviewed_at')
        db.delete_index('application_submissioninfo',['doc_reviewed_at'])
        
    
    
    models = {
        'application.address': {
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'road': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'village_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'application.applicant': {
            'activation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'doc_submission_method': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'has_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_related_model': ('IntegerListField', [], {'default': 'None'}),
            'hashed_password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'application.applicantaddress': {
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'address'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'contact_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contact_owner'", 'unique': 'True', 'to': "orm['application.Address']"}),
            'home_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'home_owner'", 'unique': 'True', 'to': "orm['application.Address']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'application.education': {
            'anet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'education'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'gat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gat_date': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gat_score_set'", 'null': 'True', 'to': "orm['application.GPExamDate']"}),
            'gpax': ('django.db.models.fields.FloatField', [], {}),
            'has_graduated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pat1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pat1_date': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pat1_score_set'", 'null': 'True', 'to': "orm['application.GPExamDate']"}),
            'pat3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pat3_date': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pat3_score_set'", 'null': 'True', 'to': "orm['application.GPExamDate']"}),
            'school_city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'school_province': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'uses_gat_score': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'application.gpexamdate': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month_year': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'application.major': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'application.majorpreference': {
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'preference'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'majors': ('IntegerListField', [], {})
        },
        'application.passwordrequestlog': {
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'password_request_log'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_request_at': ('django.db.models.fields.DateTimeField', [], {}),
            'num_requested_today': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'application.personalinfo': {
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'personal_info'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'national_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        'application.registration': {
            'activation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registrations'", 'to': "orm['application.Applicant']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'application.submissioninfo': {
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'submission_info'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'applicantion_id': ('django.db.models.fields.AutoField', [], {'unique': 'True', 'primary_key': 'True'}),
            'doc_received_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'doc_reviewed_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'doc_reviewed_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_been_reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['application']
