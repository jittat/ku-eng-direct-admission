
from south.db import db
from django.db import models
from adm.commons.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Announcement'
        db.create_table('commons_announcement', (
            ('id', orm['commons.announcement:id']),
            ('body', orm['commons.announcement:body']),
            ('created_at', orm['commons.announcement:created_at']),
        ))
        db.send_create_signal('commons', ['Announcement'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Announcement'
        db.delete_table('commons_announcement')
        
    
    
    models = {
        'commons.announcement': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['commons']
