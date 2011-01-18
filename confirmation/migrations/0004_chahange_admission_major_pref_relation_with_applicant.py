# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AdmissionMajorPreference.round_number'
        db.add_column('confirmation_admissionmajorpreference', 'round_number', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Changing field 'AdmissionMajorPreference.applicant'
        db.alter_column('confirmation_admissionmajorpreference', 'applicant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Applicant']))

        # Removing unique constraint on 'AdmissionMajorPreference', fields ['applicant']
        db.delete_unique('confirmation_admissionmajorpreference', ['applicant_id'])


    def backwards(self, orm):
        
        # Deleting field 'AdmissionMajorPreference.round_number'
        db.delete_column('confirmation_admissionmajorpreference', 'round_number')

        # Changing field 'AdmissionMajorPreference.applicant'
        db.alter_column('confirmation_admissionmajorpreference', 'applicant_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['application.Applicant']))

        # Adding unique constraint on 'AdmissionMajorPreference', fields ['applicant']
        db.create_unique('confirmation_admissionmajorpreference', ['applicant_id'])


    models = {
        'application.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'activation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'doc_submission_method': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'has_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_related_model': ('application.fields.IntegerListField', [], {'default': 'None'}),
            'hashed_password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_offline': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'national_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'confirmation.admissionconfirmation': {
            'Meta': {'object_name': 'AdmissionConfirmation'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'admission_confirmation'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'confirmed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'confirming_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'confirmation.admissionmajorpreference': {
            'Meta': {'object_name': 'AdmissionMajorPreference'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admission_major_preferences'", 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted_list': ('application.fields.IntegerListField', [], {}),
            'round_number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'confirmation.round2applicantconfirmation': {
            'Meta': {'object_name': 'Round2ApplicantConfirmation'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'round2_confirmation'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_applying_for_survey_engr': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['confirmation']
