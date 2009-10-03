
from south.db import db
from django.db import models
from adm.upload.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AppDocs'
        db.create_table('upload_appdocs', (
            ('picture', models.ImageField(storage=uploaded_storage, upload_to='hello', blank=True)),
            ('applicant', models.OneToOneField(orm['application.Applicant'])),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('upload', ['AppDocs'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AppDocs'
        db.delete_table('upload_appdocs')
        
    
    
    models = {
        'application.applicant': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'upload.appdocs': {
            'applicant': ('models.OneToOneField', ['Applicant'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'picture': ('models.ImageField', [], {'storage': 'uploaded_storage', 'upload_to': "'hello'", 'blank': 'True'})
        }
    }
    
    complete_apps = ['upload']
