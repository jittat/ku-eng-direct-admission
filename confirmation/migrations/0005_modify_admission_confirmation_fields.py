# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'AdmissionConfirmation.confirming_user'
        db.delete_column('confirmation_admissionconfirmation', 'confirming_user_id')

        # Adding field 'AdmissionConfirmation.round_number'
        db.add_column('confirmation_admissionconfirmation', 'round_number', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'AdmissionConfirmation.paid_amount'
        db.add_column('confirmation_admissionconfirmation', 'paid_amount', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Changing field 'AdmissionConfirmation.applicant'
        db.alter_column('confirmation_admissionconfirmation', 'applicant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Applicant']))

        # Removing unique constraint on 'AdmissionConfirmation', fields ['applicant']
        db.delete_unique('confirmation_admissionconfirmation', ['applicant_id'])


    def backwards(self, orm):
        
        # Adding field 'AdmissionConfirmation.confirming_user'
        db.add_column('confirmation_admissionconfirmation', 'confirming_user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']), keep_default=False)

        # Deleting field 'AdmissionConfirmation.round_number'
        db.delete_column('confirmation_admissionconfirmation', 'round_number')

        # Deleting field 'AdmissionConfirmation.paid_amount'
        db.delete_column('confirmation_admissionconfirmation', 'paid_amount')

        # Changing field 'AdmissionConfirmation.applicant'
        db.alter_column('confirmation_admissionconfirmation', 'applicant_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['application.Applicant']))

        # Adding unique constraint on 'AdmissionConfirmation', fields ['applicant']
        db.create_unique('confirmation_admissionconfirmation', ['applicant_id'])


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
        'confirmation.admissionconfirmation': {
            'Meta': {'object_name': 'AdmissionConfirmation'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admission_confirmations'", 'to': "orm['application.Applicant']"}),
            'confirmed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round_number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        }
    }

    complete_apps = ['confirmation']
