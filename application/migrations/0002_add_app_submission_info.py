# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.application.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Applicant.doc_submission_method'
        db.add_column('application_applicant', 'doc_submission_method', models.IntegerField(default=0))
        
        # Adding field 'Applicant.is_submitted'
        db.add_column('application_applicant', 'is_submitted', models.BooleanField(default=False))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Applicant.doc_submission_method'
        db.delete_column('application_applicant', 'doc_submission_method')
        
        # Deleting field 'Applicant.is_submitted'
        db.delete_column('application_applicant', 'is_submitted')
        
    
    
    models = {
        'application.address': {
            'city': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb8\xad\xe0\xb8\xb3\xe0\xb9\x80\xe0\xb8\xa0\xe0\xb8\xad/\xe0\xb9\x80\xe0\xb8\x82\xe0\xb8\x95"'}),
            'district': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb8\x95\xe0\xb8\xb3\xe0\xb8\x9a\xe0\xb8\xa5/\xe0\xb9\x81\xe0\xb8\x82\xe0\xb8\xa7\xe0\xb8\x87"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'number': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb8\x9a\xe0\xb9\x89\xe0\xb8\xb2\xe0\xb8\x99\xe0\xb9\x80\xe0\xb8\xa5\xe0\xb8\x82\xe0\xb8\x97\xe0\xb8\xb5\xe0\xb9\x88"'}),
            'phone_number': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb8\xab\xe0\xb8\xa1\xe0\xb8\xb2\xe0\xb8\xa2\xe0\xb9\x80\xe0\xb8\xa5\xe0\xb8\x82\xe0\xb9\x82\xe0\xb8\x97\xe0\xb8\xa3\xe0\xb8\xa8\xe0\xb8\xb1\xe0\xb8\x9e\xe0\xb8\x97\xe0\xb9\x8c"'}),
            'postal_code': ('models.CharField', [], {'max_length': '10', 'verbose_name': '"\xe0\xb8\xa3\xe0\xb8\xab\xe0\xb8\xb1\xe0\xb8\xaa\xe0\xb9\x84\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xa9\xe0\xb8\x93\xe0\xb8\xb5\xe0\xb8\xa2\xe0\xb9\x8c"'}),
            'province': ('models.CharField', [], {'max_length': '25', 'verbose_name': '"\xe0\xb8\x88\xe0\xb8\xb1\xe0\xb8\x87\xe0\xb8\xab\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x94"'}),
            'road': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb8\x96\xe0\xb8\x99\xe0\xb8\x99"'}),
            'village_name': ('models.CharField', [], {'max_length': '100', 'verbose_name': '"\xe0\xb8\xab\xe0\xb8\xa1\xe0\xb8\xb9\xe0\xb9\x88\xe0\xb8\x9a\xe0\xb9\x89\xe0\xb8\xb2\xe0\xb8\x99"', 'blank': 'True'}),
            'village_number': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\xab\xe0\xb8\xa1\xe0\xb8\xb9\xe0\xb9\x88\xe0\xb8\x97\xe0\xb8\xb5\xe0\xb9\x88"', 'blank': 'True'})
        },
        'application.applicantaddress': {
            'applicant': ('models.OneToOneField', ['Applicant'], {'related_name': '"address"'}),
            'contact_address': ('models.OneToOneField', ['Address'], {'related_name': '"contact_owner"'}),
            'home_address': ('models.OneToOneField', ['Address'], {'related_name': '"home_owner"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'application.education': {
            'anet': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 A-NET"', 'blank': 'True'}),
            'applicant': ('models.OneToOneField', ['Applicant'], {'related_name': '"education"'}),
            'gat': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 GAT"', 'blank': 'True'}),
            'gat_date': ('models.ForeignKey', ['GPExamDate'], {'related_name': '"gat_score_set"', 'null': 'True', 'verbose_name': '"\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x99\xe0\xb8\xaa\xe0\xb8\xad\xe0\xb8\x9a GAT"', 'blank': 'True'}),
            'gpax': ('models.FloatField', [], {'verbose_name': '"GPAX"'}),
            'has_graduated': ('models.BooleanField', [], {'verbose_name': 'u"\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb8\x94\xe0\xb8\xb1\xe0\xb8\x9a\xe0\xb8\x81\xe0\xb8\xb2\xe0\xb8\xa3\xe0\xb8\xa8\xe0\xb8\xb6\xe0\xb8\x81\xe0\xb8\xa9\xe0\xb8\xb2"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'pat1': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 PAT 1"', 'blank': 'True'}),
            'pat1_date': ('models.ForeignKey', ['GPExamDate'], {'related_name': '"pat1_score_set"', 'null': 'True', 'verbose_name': '"\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x99\xe0\xb8\xaa\xe0\xb8\xad\xe0\xb8\x9a PAT 1"', 'blank': 'True'}),
            'pat3': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 PAT 3"', 'blank': 'True'}),
            'pat3_date': ('models.ForeignKey', ['GPExamDate'], {'related_name': '"pat3_score_set"', 'null': 'True', 'verbose_name': '"\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x99\xe0\xb8\xaa\xe0\xb8\xad\xe0\xb8\x9a PAT 3"', 'blank': 'True'}),
            'school_city': ('models.CharField', [], {'max_length': '50', 'verbose_name': 'u"\xe0\xb8\xad\xe0\xb8\xb3\xe0\xb9\x80\xe0\xb8\xa0\xe0\xb8\xad/\xe0\xb9\x80\xe0\xb8\x82\xe0\xb8\x95"'}),
            'school_name': ('models.CharField', [], {'max_length': '100', 'verbose_name': 'u"\xe0\xb9\x82\xe0\xb8\xa3\xe0\xb8\x87\xe0\xb9\x80\xe0\xb8\xa3\xe0\xb8\xb5\xe0\xb8\xa2\xe0\xb8\x99"'}),
            'school_province': ('models.CharField', [], {'max_length': '25', 'verbose_name': 'u"\xe0\xb8\x88\xe0\xb8\xb1\xe0\xb8\x87\xe0\xb8\xab\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x94"'}),
            'uses_gat_score': ('models.BooleanField', [], {'verbose_name': 'u"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99\xe0\xb8\x97\xe0\xb8\xb5\xe0\xb9\x88\xe0\xb9\x83\xe0\xb8\x8a\xe0\xb9\x89\xe0\xb8\xaa\xe0\xb8\xa1\xe0\xb8\xb1\xe0\xb8\x84\xe0\xb8\xa3"'})
        },
        'application.majorpreference': {
            'applicant': ('models.OneToOneField', ['Applicant'], {'related_name': '"preference"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'majors': ('IntegerListField', [], {})
        },
        'application.major': {
            'Meta': {'ordering': "['number']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'}),
            'number': ('models.CharField', [], {'max_length': '5'})
        },
        'application.applicant': {
            'birth_date': ('models.DateField', [], {'verbose_name': '"\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x99\xe0\xb9\x80\xe0\xb8\x81\xe0\xb8\xb4\xe0\xb8\x94"'}),
            'doc_submission_method': ('models.IntegerField', [], {'default': '0'}),
            'email': ('models.EmailField', [], {}),
            'ethnicity': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb9\x80\xe0\xb8\x8a\xe0\xb8\xb7\xe0\xb9\x89\xe0\xb8\xad\xe0\xb8\x8a\xe0\xb8\xb2\xe0\xb8\x95\xe0\xb8\xb4"'}),
            'first_name': ('models.CharField', [], {'max_length': '200', 'verbose_name': '"\xe0\xb8\x8a\xe0\xb8\xb7\xe0\xb9\x88\xe0\xb8\xad"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_submitted': ('models.BooleanField', [], {'default': 'False'}),
            'last_name': ('models.CharField', [], {'max_length': '300', 'verbose_name': '"\xe0\xb8\x99\xe0\xb8\xb2\xe0\xb8\xa1\xe0\xb8\xaa\xe0\xb8\x81\xe0\xb8\xb8\xe0\xb8\xa5"'}),
            'national_id': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb9\x80\xe0\xb8\xa5\xe0\xb8\x82\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb8\x88\xe0\xb8\xb3\xe0\xb8\x95\xe0\xb8\xb1\xe0\xb8\xa7\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb8\x8a\xe0\xb8\xb2\xe0\xb8\x8a\xe0\xb8\x99"'}),
            'nationality': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb8\xaa\xe0\xb8\xb1\xe0\xb8\x8d\xe0\xb8\x8a\xe0\xb8\xb2\xe0\xb8\x95\xe0\xb8\xb4"'}),
            'phone_number': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb8\xab\xe0\xb8\xa1\xe0\xb8\xb2\xe0\xb8\xa2\xe0\xb9\x80\xe0\xb8\xa5\xe0\xb8\x82\xe0\xb9\x82\xe0\xb8\x97\xe0\xb8\xa3\xe0\xb8\xa8\xe0\xb8\xb1\xe0\xb8\x9e\xe0\xb8\x97\xe0\xb9\x8c"'})
        },
        'application.gpexamdate': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'month_year': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb9\x80\xe0\xb8\x94\xe0\xb8\xb7\xe0\xb8\xad\xe0\xb8\x99\xe0\xb9\x81\xe0\xb8\xa5\xe0\xb8\xb0\xe0\xb8\x9b\xe0\xb8\xb5\xe0\xb8\x82\xe0\xb8\xad\xe0\xb8\x87\xe0\xb8\x81\xe0\xb8\xb2\xe0\xb8\xa3\xe0\xb8\xaa\xe0\xb8\xad\xe0\xb8\x9a"'})
        },
        'application.applicantaccount': {
            'applicant': ('models.OneToOneField', ['Applicant'], {}),
            'hashed_password': ('models.CharField', [], {'max_length': '100'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['application']
