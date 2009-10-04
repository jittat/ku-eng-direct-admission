# _*_  coding: utf-8 _*_

from south.db import db
from django.db import models
from adm.upload.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AppDocs'
        db.create_table('upload_appdocs', (
            ('picture', models.ImageField(storage=uploaded_storage, verbose_name='รูปถ่าย', upload_to='hello', blank=True)),
            ('edu_certificate', models.ImageField(storage=uploaded_storage, verbose_name='ใบรับรองการศึกษา', upload_to='hello', blank=True)),
            ('pat1_score', models.ImageField(storage=uploaded_storage, verbose_name='คะแนน PAT1', upload_to='hello', blank=True)),
            ('applicant', models.OneToOneField(orm['application.Applicant'])),
            ('abroad_edu_certificate', models.ImageField(storage=uploaded_storage, verbose_name='หลักฐานการศึกษาต่างประเทศ', upload_to='hello', blank=True)),
            ('app_fee_doc', models.ImageField(storage=uploaded_storage, verbose_name='หลักฐานใบนำฝากเงินค่าสมัคร', upload_to='hello', blank=True)),
            ('pat3_score', models.ImageField(storage=uploaded_storage, verbose_name='คะแนน PAT3', upload_to='hello', blank=True)),
            ('anet_score', models.ImageField(storage=uploaded_storage, verbose_name='คะแนน A-NET ความถนัดทางวิศวกรรม', upload_to='hello', blank=True)),
            ('nat_id', models.ImageField(storage=uploaded_storage, verbose_name='สำเนาบัตรประจำตัวประชาชน หรือสำเนาบัตรนักเรียน', upload_to='hello', blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('gat_score', models.ImageField(storage=uploaded_storage, verbose_name='คะแนน GAT', upload_to='hello', blank=True)),
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
            'abroad_edu_certificate': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb8\xab\xe0\xb8\xa5\xe0\xb8\xb1\xe0\xb8\x81\xe0\xb8\x90\xe0\xb8\xb2\xe0\xb8\x99\xe0\xb8\x81\xe0\xb8\xb2\xe0\xb8\xa3\xe0\xb8\xa8\xe0\xb8\xb6\xe0\xb8\x81\xe0\xb8\xa9\xe0\xb8\xb2\xe0\xb8\x95\xe0\xb9\x88\xe0\xb8\xb2\xe0\xb8\x87\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb9\x80\xe0\xb8\x97\xe0\xb8\xa8'", 'upload_to': "'hello'", 'blank': 'True'}),
            'anet_score': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 A-NET \xe0\xb8\x84\xe0\xb8\xa7\xe0\xb8\xb2\xe0\xb8\xa1\xe0\xb8\x96\xe0\xb8\x99\xe0\xb8\xb1\xe0\xb8\x94\xe0\xb8\x97\xe0\xb8\xb2\xe0\xb8\x87\xe0\xb8\xa7\xe0\xb8\xb4\xe0\xb8\xa8\xe0\xb8\xa7\xe0\xb8\x81\xe0\xb8\xa3\xe0\xb8\xa3\xe0\xb8\xa1'", 'upload_to': "'hello'", 'blank': 'True'}),
            'app_fee_doc': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb8\xab\xe0\xb8\xa5\xe0\xb8\xb1\xe0\xb8\x81\xe0\xb8\x90\xe0\xb8\xb2\xe0\xb8\x99\xe0\xb9\x83\xe0\xb8\x9a\xe0\xb8\x99\xe0\xb8\xb3\xe0\xb8\x9d\xe0\xb8\xb2\xe0\xb8\x81\xe0\xb9\x80\xe0\xb8\x87\xe0\xb8\xb4\xe0\xb8\x99\xe0\xb8\x84\xe0\xb9\x88\xe0\xb8\xb2\xe0\xb8\xaa\xe0\xb8\xa1\xe0\xb8\xb1\xe0\xb8\x84\xe0\xb8\xa3'", 'upload_to': "'hello'", 'blank': 'True'}),
            'applicant': ('models.OneToOneField', ['Applicant'], {}),
            'edu_certificate': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb9\x83\xe0\xb8\x9a\xe0\xb8\xa3\xe0\xb8\xb1\xe0\xb8\x9a\xe0\xb8\xa3\xe0\xb8\xad\xe0\xb8\x87\xe0\xb8\x81\xe0\xb8\xb2\xe0\xb8\xa3\xe0\xb8\xa8\xe0\xb8\xb6\xe0\xb8\x81\xe0\xb8\xa9\xe0\xb8\xb2'", 'upload_to': "'hello'", 'blank': 'True'}),
            'gat_score': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 GAT'", 'upload_to': "'hello'", 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'nat_id': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb8\xaa\xe0\xb8\xb3\xe0\xb9\x80\xe0\xb8\x99\xe0\xb8\xb2\xe0\xb8\x9a\xe0\xb8\xb1\xe0\xb8\x95\xe0\xb8\xa3\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb8\x88\xe0\xb8\xb3\xe0\xb8\x95\xe0\xb8\xb1\xe0\xb8\xa7\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb8\x8a\xe0\xb8\xb2\xe0\xb8\x8a\xe0\xb8\x99 \xe0\xb8\xab\xe0\xb8\xa3\xe0\xb8\xb7\xe0\xb8\xad\xe0\xb8\xaa\xe0\xb8\xb3\xe0\xb9\x80\xe0\xb8\x99\xe0\xb8\xb2\xe0\xb8\x9a\xe0\xb8\xb1\xe0\xb8\x95\xe0\xb8\xa3\xe0\xb8\x99\xe0\xb8\xb1\xe0\xb8\x81\xe0\xb9\x80\xe0\xb8\xa3\xe0\xb8\xb5\xe0\xb8\xa2\xe0\xb8\x99'", 'upload_to': "'hello'", 'blank': 'True'}),
            'pat1_score': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 PAT1'", 'upload_to': "'hello'", 'blank': 'True'}),
            'pat3_score': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 PAT3'", 'upload_to': "'hello'", 'blank': 'True'}),
            'picture': ('models.ImageField', [], {'storage': 'uploaded_storage', 'verbose_name': "'\xe0\xb8\xa3\xe0\xb8\xb9\xe0\xb8\x9b\xe0\xb8\x96\xe0\xb9\x88\xe0\xb8\xb2\xe0\xb8\xa2'", 'upload_to': "'hello'", 'blank': 'True'})
        }
    }
    
    complete_apps = ['upload']
