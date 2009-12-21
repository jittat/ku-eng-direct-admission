
from south.db import db
from django.db import models
from adm.commons.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Log'
        db.create_table('commons_log', (
            ('id', orm['commons.log:id']),
            ('user', orm['commons.log:user']),
            ('message', orm['commons.log:message']),
            ('created_at', orm['commons.log:created_at']),
            ('updated_at', orm['commons.log:updated_at']),
        ))
        db.send_create_signal('commons', ['Log'])
        
        # Changing field 'Announcement.created_at'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column('commons_announcement', 'created_at', orm['commons.announcement:created_at'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Log'
        db.delete_table('commons_log')
        
        # Changing field 'Announcement.created_at'
        # (to signature: django.db.models.fields.DateTimeField(auto_now_add=True, blank=True))
        db.alter_column('commons_announcement', 'created_at', orm['commons.announcement:created_at'])
        
    
    
    models = {
        'commons.announcement': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'commons.log': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }
    
    complete_apps = ['commons']
