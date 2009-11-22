
from south.db import db
from django.db import models
from adm.commons.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Announcement.is_enabled'
        db.add_column('commons_announcement', 'is_enabled', orm['commons.announcement:is_enabled'])
        db.create_index('commons_announcement', ['is_enabled'])
    
    
    def backwards(self, orm):
        
        # Deleting field 'Announcement.is_enabled'
        db.delete_column('commons_announcement', 'is_enabled')
        db.delete_index('commons_announcement', ['is_enabled'])
        
    
    
    models = {
        'commons.announcement': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['commons']
