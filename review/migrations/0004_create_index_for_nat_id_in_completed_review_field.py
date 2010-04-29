# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding index on 'CompletedReviewField', fields ['national_id']
        db.create_index('review_completedreviewfield', ['national_id'])
    
    
    def backwards(self, orm):
        
        # Removing index on 'CompletedReviewField', fields ['national_id']
        db.delete_index('review_completedreviewfield', ['national_id'])
    
    
    models = {
        'application.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'activation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'doc_submission_method': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'has_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_related_model': ('application.fields.IntegerListField', [], {'default': 'None'}),
            'hashed_password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_offline': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'review.completedreviewfield': {
            'Meta': {'object_name': 'CompletedReviewField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'national_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'review_field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['review.ReviewField']"})
        },
        'review.reviewfield': {
            'Meta': {'object_name': 'ReviewField'},
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
            'Meta': {'object_name': 'ReviewFieldResult'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Applicant']"}),
            'applicant_note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'is_passed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'review_field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['review.ReviewField']"})
        }
    }
    
    complete_apps = ['review']
