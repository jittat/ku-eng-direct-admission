# -*-  coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.upload.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'AppDocs.num_uploaded_today'
        db.add_column('upload_appdocs', 'num_uploaded_today', orm['upload.appdocs:num_uploaded_today'])
        
        # Adding field 'AppDocs.last_uploaded_at'
        db.add_column('upload_appdocs', 'last_uploaded_at', orm['upload.appdocs:last_uploaded_at'])
        
        # Changing field 'AppDocs.pat1_score'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'pat1_score', orm['upload.appdocs:pat1_score'])
        
        # Changing field 'AppDocs.pat3_score'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'pat3_score', orm['upload.appdocs:pat3_score'])
        
        # Changing field 'AppDocs.picture'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'picture', orm['upload.appdocs:picture'])
        
        # Changing field 'AppDocs.abroad_edu_certificate'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'abroad_edu_certificate', orm['upload.appdocs:abroad_edu_certificate'])
        
        # Changing field 'AppDocs.app_fee_doc'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'app_fee_doc', orm['upload.appdocs:app_fee_doc'])
        
        # Changing field 'AppDocs.edu_certificate'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'edu_certificate', orm['upload.appdocs:edu_certificate'])
        
        # Changing field 'AppDocs.anet_score'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'anet_score', orm['upload.appdocs:anet_score'])
        
        # Changing field 'AppDocs.nat_id'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'nat_id', orm['upload.appdocs:nat_id'])
        
        # Changing field 'AppDocs.gat_score'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100, blank=True))
        db.alter_column('upload_appdocs', 'gat_score', orm['upload.appdocs:gat_score'])
        
        # Creating unique_together for [applicant] on AppDocs.
        db.create_unique('upload_appdocs', ['applicant_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [applicant] on AppDocs.
        db.delete_unique('upload_appdocs', ['applicant_id'])
        
        # Deleting field 'AppDocs.num_uploaded_today'
        db.delete_column('upload_appdocs', 'num_uploaded_today')
        
        # Deleting field 'AppDocs.last_uploaded_at'
        db.delete_column('upload_appdocs', 'last_uploaded_at')
        
        # Changing field 'AppDocs.pat1_score'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'pat1_score', orm['upload.appdocs:pat1_score'])
        
        # Changing field 'AppDocs.pat3_score'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'pat3_score', orm['upload.appdocs:pat3_score'])
        
        # Changing field 'AppDocs.picture'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'picture', orm['upload.appdocs:picture'])
        
        # Changing field 'AppDocs.abroad_edu_certificate'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'abroad_edu_certificate', orm['upload.appdocs:abroad_edu_certificate'])
        
        # Changing field 'AppDocs.app_fee_doc'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'app_fee_doc', orm['upload.appdocs:app_fee_doc'])
        
        # Changing field 'AppDocs.edu_certificate'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'edu_certificate', orm['upload.appdocs:edu_certificate'])
        
        # Changing field 'AppDocs.anet_score'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'anet_score', orm['upload.appdocs:anet_score'])
        
        # Changing field 'AppDocs.nat_id'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'nat_id', orm['upload.appdocs:nat_id'])
        
        # Changing field 'AppDocs.gat_score'
        # (to signature: models.ImageField(blank=True, storage=uploaded_storage))
        db.alter_column('upload_appdocs', 'gat_score', orm['upload.appdocs:gat_score'])
        
    
    
    models = {
        'application.applicant': {
            'activation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'doc_submission_method': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'has_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hashed_password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'upload.appdocs': {
            'abroad_edu_certificate': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'anet_score': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'app_fee_doc': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['application.Applicant']", 'unique': 'True'}),
            'edu_certificate': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'gat_score': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'default':'"2009-01-01 00:00"'}),
            'nat_id': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'num_uploaded_today': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pat1_score': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'pat3_score': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        }
    }
    
    complete_apps = ['upload']
