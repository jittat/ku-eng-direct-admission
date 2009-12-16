
from south.db import db
from django.db import models
from adm.supplement.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Supplement.uploaded_at'
        db.add_column('supplement_supplement', 'uploaded_at', orm['supplement.supplement:uploaded_at'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Supplement.uploaded_at'
        db.delete_column('supplement_supplement', 'uploaded_at')
        
    
    
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
        'supplement.supplement': {
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplements'", 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'supplement_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplement.SupplementType']"}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'supplement.supplementtype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        }
    }
    
    complete_apps = ['supplement']
