# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.review.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'ReviewField.short_name'
        db.add_column('review_reviewfield', 'short_name', orm['review.reviewfield:short_name'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'ReviewField.short_name'
        db.delete_column('review_reviewfield', 'short_name')
        
    
    
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
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'review.reviewfield': {
            'admin_note_format': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'admin_note_help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'applicant_note_format': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'applicant_note_help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'review.reviewfieldresult': {
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Applicant']"}),
            'applicant_note': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_note': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'is_passed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'review_field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['review.ReviewField']"})
        }
    }
    
    complete_apps = ['review']
