
from south.db import db
from django.db import models
from adm.manual.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AdminEditLog'
        db.create_table('manual_admineditlog', (
            ('id', orm['manual.AdminEditLog:id']),
            ('applicant', orm['manual.AdminEditLog:applicant']),
            ('message', orm['manual.AdminEditLog:message']),
        ))
        db.send_create_signal('manual', ['AdminEditLog'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AdminEditLog'
        db.delete_table('manual_admineditlog')
        
    
    
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
        'manual.admineditlog': {
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {})
        }
    }
    
    complete_apps = ['manual']
