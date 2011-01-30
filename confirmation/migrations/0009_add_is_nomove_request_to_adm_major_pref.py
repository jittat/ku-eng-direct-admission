# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AdmissionMajorPreference.is_nomove_request'
        db.add_column('confirmation_admissionmajorpreference', 'is_nomove_request', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Changing field 'StudentRegistration.passport_number'
        db.alter_column('confirmation_studentregistration', 'passport_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True))


    def backwards(self, orm):
        
        # Deleting field 'AdmissionMajorPreference.is_nomove_request'
        db.delete_column('confirmation_admissionmajorpreference', 'is_nomove_request')

        # Changing field 'StudentRegistration.passport_number'
        db.alter_column('confirmation_studentregistration', 'passport_number', self.gf('django.db.models.fields.CharField')(max_length=40))


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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted_list': ('application.fields.IntegerListField', [], {}),
            'is_nomove_request': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
        'confirmation.studentregistration': {
            'Meta': {'object_name': 'StudentRegistration'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'student_registration'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cell_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'english_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'english_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'father_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'father_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'father_national_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'father_title': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'home_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mother_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mother_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'mother_national_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mother_title': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'passport_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['confirmation']
