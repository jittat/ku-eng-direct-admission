# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.review.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ReviewFieldResult'
        db.create_table('review_reviewfieldresult', (
            ('id', orm['review.ReviewFieldResult:id']),
            ('applicant', orm['review.ReviewFieldResult:applicant']),
            ('review_field', orm['review.ReviewFieldResult:review_field']),
            ('is_passed', orm['review.ReviewFieldResult:is_passed']),
            ('applicant_note', orm['review.ReviewFieldResult:applicant_note']),
            ('internal_note', orm['review.ReviewFieldResult:internal_note']),
        ))
        db.send_create_signal('review', ['ReviewFieldResult'])
        
        # Adding model 'ReviewField'
        db.create_table('review_reviewfield', (
            ('id', orm['review.ReviewField:id']),
            ('name', orm['review.ReviewField:name']),
            ('order', orm['review.ReviewField:order']),
            ('required', orm['review.ReviewField:required']),
            ('enabled', orm['review.ReviewField:enabled']),
            ('applicant_note_help_text', orm['review.ReviewField:applicant_note_help_text']),
            ('admin_note_help_text', orm['review.ReviewField:admin_note_help_text']),
            ('applicant_note_format', orm['review.ReviewField:applicant_note_format']),
            ('admin_note_format', orm['review.ReviewField:admin_note_format']),
        ))
        db.send_create_signal('review', ['ReviewField'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ReviewFieldResult'
        db.delete_table('review_reviewfieldresult')
        
        # Deleting model 'ReviewField'
        db.delete_table('review_reviewfield')
        
    
    
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
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
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
