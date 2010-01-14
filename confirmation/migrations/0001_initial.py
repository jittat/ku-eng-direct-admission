
from south.db import db
from django.db import models
from adm.confirmation.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AdmissionMajorPreference'
        db.create_table('confirmation_admissionmajorpreference', (
            ('id', orm['confirmation.AdmissionMajorPreference:id']),
            ('applicant', orm['confirmation.AdmissionMajorPreference:applicant']),
            ('is_accepted_list', orm['confirmation.AdmissionMajorPreference:is_accepted_list']),
        ))
        db.send_create_signal('confirmation', ['AdmissionMajorPreference'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AdmissionMajorPreference'
        db.delete_table('confirmation_admissionmajorpreference')
        
    
    
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
        'confirmation.admissionmajorpreference': {
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'admission_major_preference'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted_list': ('IntegerListField', [], {})
        }
    }
    
    complete_apps = ['confirmation']
