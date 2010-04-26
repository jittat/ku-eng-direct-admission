# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Feature'
        db.create_table('feature_switch_feature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('feature_switch', ['Feature'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Feature'
        db.delete_table('feature_switch_feature')
    
    
    models = {
        'feature_switch.feature': {
            'Meta': {'object_name': 'Feature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }
    
    complete_apps = ['feature_switch']
