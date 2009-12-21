
from south.db import db
from django.db import models
from adm.commons.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Log.applicant_id'
        db.add_column('commons_log', 'applicant_id', orm['commons.log:applicant_id'])
        
        # Adding field 'Log.applicantion_id'
        db.add_column('commons_log', 'applicantion_id', orm['commons.log:applicantion_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Log.applicant_id'
        db.delete_column('commons_log', 'applicant_id')
        
        # Deleting field 'Log.applicantion_id'
        db.delete_column('commons_log', 'applicantion_id')
        
    
    
    models = {
        'commons.announcement': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'commons.log': {
            'applicant_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'applicantion_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }
    
    complete_apps = ['commons']
