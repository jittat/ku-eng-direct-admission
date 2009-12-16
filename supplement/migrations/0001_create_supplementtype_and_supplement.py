
from south.db import db
from django.db import models
from adm.supplement.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Supplement'
        db.create_table('supplement_supplement', (
            ('id', orm['supplement.Supplement:id']),
            ('applicant', orm['supplement.Supplement:applicant']),
            ('supplement_type', orm['supplement.Supplement:supplement_type']),
            ('image', orm['supplement.Supplement:image']),
        ))
        db.send_create_signal('supplement', ['Supplement'])
        
        # Adding model 'SupplementType'
        db.create_table('supplement_supplementtype', (
            ('id', orm['supplement.SupplementType:id']),
            ('name', orm['supplement.SupplementType:name']),
            ('order', orm['supplement.SupplementType:order']),
        ))
        db.send_create_signal('supplement', ['SupplementType'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Supplement'
        db.delete_table('supplement_supplement')
        
        # Deleting model 'SupplementType'
        db.delete_table('supplement_supplementtype')
        
    
    
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
            'supplement_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['supplement.SupplementType']"})
        },
        'supplement.supplementtype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        }
    }
    
    complete_apps = ['supplement']
