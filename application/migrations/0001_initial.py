# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from adm.application.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Address'
        db.create_table('application_address', (
            ('province', models.CharField(max_length=25, verbose_name="จังหวัด")),
            ('city', models.CharField(max_length=50, verbose_name="อำเภอ/เขต")),
            ('village_number', models.IntegerField(null=True, verbose_name="หมู่ที่", blank=True)),
            ('district', models.CharField(max_length=50, verbose_name="ตำบล/แขวง")),
            ('number', models.CharField(max_length=20, verbose_name="บ้านเลขที่")),
            ('postal_code', models.CharField(max_length=10, verbose_name="รหัสไปรษณีย์")),
            ('village_name', models.CharField(max_length=100, verbose_name="หมู่บ้าน", blank=True)),
            ('phone_number', models.CharField(max_length=20, verbose_name="หมายเลขโทรศัพท์")),
            ('id', models.AutoField(primary_key=True)),
            ('road', models.CharField(max_length=50, verbose_name="ถนน")),
        ))
        db.send_create_signal('application', ['Address'])
        
        # Adding model 'Major'
        db.create_table('application_major', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
            ('number', models.CharField(max_length=5)),
        ))
        db.send_create_signal('application', ['Major'])
        
        # Adding model 'Education'
        db.create_table('application_education', (
            ('pat1', models.IntegerField(null=True, verbose_name="คะแนน PAT 1", blank=True)),
            ('pat3', models.IntegerField(null=True, verbose_name="คะแนน PAT 3", blank=True)),
            ('gat', models.IntegerField(null=True, verbose_name="คะแนน GAT", blank=True)),
            ('anet', models.IntegerField(null=True, verbose_name="คะแนน A-NET", blank=True)),
            ('pat3_date', models.ForeignKey(orm.GPExamDate, related_name="pat3_score_set", null=True, verbose_name="วันสอบ PAT 3", blank=True)),
            ('uses_gat_score', models.BooleanField(verbose_name=u"คะแนนที่ใช้สมัคร")),
            ('gat_date', models.ForeignKey(orm.GPExamDate, related_name="gat_score_set", null=True, verbose_name="วันสอบ GAT", blank=True)),
            ('applicant', models.OneToOneField(orm.Applicant, related_name="education")),
            ('school_province', models.CharField(max_length=25, verbose_name=u"จังหวัด")),
            ('school_name', models.CharField(max_length=100, verbose_name=u"โรงเรียน")),
            ('pat1_date', models.ForeignKey(orm.GPExamDate, related_name="pat1_score_set", null=True, verbose_name="วันสอบ PAT 1", blank=True)),
            ('school_city', models.CharField(max_length=50, verbose_name=u"อำเภอ/เขต")),
            ('has_graduated', models.BooleanField(verbose_name=u"ระดับการศึกษา")),
            ('gpax', models.FloatField(verbose_name="GPAX")),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('application', ['Education'])
        
        # Adding model 'MajorPreference'
        db.create_table('application_majorpreference', (
            ('majors', IntegerListField()),
            ('applicant', models.OneToOneField(orm.Applicant, related_name="preference")),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('application', ['MajorPreference'])
        
        # Adding model 'ApplicantAddress'
        db.create_table('application_applicantaddress', (
            ('contact_address', models.OneToOneField(orm.Address, related_name="contact_owner")),
            ('applicant', models.OneToOneField(orm.Applicant, related_name="address")),
            ('home_address', models.OneToOneField(orm.Address, related_name="home_owner")),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('application', ['ApplicantAddress'])
        
        # Adding model 'Applicant'
        db.create_table('application_applicant', (
            ('phone_number', models.CharField(max_length=20, verbose_name="หมายเลขโทรศัพท์")),
            ('first_name', models.CharField(max_length=200, verbose_name="ชื่อ")),
            ('last_name', models.CharField(max_length=300, verbose_name="นามสกุล")),
            ('national_id', models.CharField(max_length=20, verbose_name="เลขประจำตัวประชาชน")),
            ('email', models.EmailField()),
            ('birth_date', models.DateField(verbose_name="วันเกิด")),
            ('nationality', models.CharField(max_length=50, verbose_name="สัญชาติ")),
            ('id', models.AutoField(primary_key=True)),
            ('ethnicity', models.CharField(max_length=50, verbose_name="เชื้อชาติ")),
        ))
        db.send_create_signal('application', ['Applicant'])
        
        # Adding model 'GPExamDate'
        db.create_table('application_gpexamdate', (
            ('month_year', models.CharField(max_length=20, verbose_name="เดือนและปีของการสอบ")),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('application', ['GPExamDate'])
        
        # Adding model 'ApplicantAccount'
        db.create_table('application_applicantaccount', (
            ('hashed_password', models.CharField(max_length=100)),
            ('applicant', models.OneToOneField(orm.Applicant)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('application', ['ApplicantAccount'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Address'
        db.delete_table('application_address')
        
        # Deleting model 'Major'
        db.delete_table('application_major')
        
        # Deleting model 'Education'
        db.delete_table('application_education')
        
        # Deleting model 'MajorPreference'
        db.delete_table('application_majorpreference')
        
        # Deleting model 'ApplicantAddress'
        db.delete_table('application_applicantaddress')
        
        # Deleting model 'Applicant'
        db.delete_table('application_applicant')
        
        # Deleting model 'GPExamDate'
        db.delete_table('application_gpexamdate')
        
        # Deleting model 'ApplicantAccount'
        db.delete_table('application_applicantaccount')
        
    
    
    models = {
        'application.address': {
            'city': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb8\xad\xe0\xb8\xb3\xe0\xb9\x80\xe0\xb8\xa0\xe0\xb8\xad/\xe0\xb9\x80\xe0\xb8\x82\xe0\xb8\x95"'}),
            'district': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb8\x95\xe0\xb8\xb3\xe0\xb8\x9a\xe0\xb8\xa5/\xe0\xb9\x81\xe0\xb8\x82\xe0\xb8\xa7\xe0\xb8\x87"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'number': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb8\x9a\xe0\xb9\x89\xe0\xb8\xb2\xe0\xb8\x99\xe0\xb9\x80\xe0\xb8\xa5\xe0\xb8\x82\xe0\xb8\x97\xe0\xb8\xb5\xe0\xb9\x88"'}),
            'phone_number': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb8\xab\xe0\xb8\xa1\xe0\xb8\xb2\xe0\xb8\xa2\xe0\xb9\x80\xe0\xb8\xa5\xe0\xb8\x82\xe0\xb9\x82\xe0\xb8\x97\xe0\xb8\xa3\xe0\xb8\xa8\xe0\xb8\xb1\xe0\xb8\x9e\xe0\xb8\x97\xe0\xb9\x8c"'}),
            'postal_code': ('models.CharField', [], {'max_length': '10', 'verbose_name': '"\xe0\xb8\xa3\xe0\xb8\xab\xe0\xb8\xb1\xe0\xb8\xaa\xe0\xb9\x84\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xa9\xe0\xb8\x93\xe0\xb8\xb5\xe0\xb8\xa2\xe0\xb9\x8c"'}),
            'province': ('models.CharField', [], {'max_length': '25', 'verbose_name': '"\xe0\xb8\x88\xe0\xb8\xb1\xe0\xb8\x87\xe0\xb8\xab\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x94"'}),
            'road': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb8\x96\xe0\xb8\x99\xe0\xb8\x99"'}),
            'village_name': ('models.CharField', [], {'max_length': '100', 'verbose_name': '"\xe0\xb8\xab\xe0\xb8\xa1\xe0\xb8\xb9\xe0\xb9\x88\xe0\xb8\x9a\xe0\xb9\x89\xe0\xb8\xb2\xe0\xb8\x99"', 'blank': 'True'}),
            'village_number': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\xab\xe0\xb8\xa1\xe0\xb8\xb9\xe0\xb9\x88\xe0\xb8\x97\xe0\xb8\xb5\xe0\xb9\x88"', 'blank': 'True'})
        },
        'application.applicantaddress': {
            'applicant': ('models.OneToOneField', ['Applicant'], {'related_name': '"address"'}),
            'contact_address': ('models.OneToOneField', ['Address'], {'related_name': '"contact_owner"'}),
            'home_address': ('models.OneToOneField', ['Address'], {'related_name': '"home_owner"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'application.education': {
            'anet': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 A-NET"', 'blank': 'True'}),
            'applicant': ('models.OneToOneField', ['Applicant'], {'related_name': '"education"'}),
            'gat': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 GAT"', 'blank': 'True'}),
            'gat_date': ('models.ForeignKey', ['GPExamDate'], {'related_name': '"gat_score_set"', 'null': 'True', 'verbose_name': '"\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x99\xe0\xb8\xaa\xe0\xb8\xad\xe0\xb8\x9a GAT"', 'blank': 'True'}),
            'gpax': ('models.FloatField', [], {'verbose_name': '"GPAX"'}),
            'has_graduated': ('models.BooleanField', [], {'verbose_name': 'u"\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb8\x94\xe0\xb8\xb1\xe0\xb8\x9a\xe0\xb8\x81\xe0\xb8\xb2\xe0\xb8\xa3\xe0\xb8\xa8\xe0\xb8\xb6\xe0\xb8\x81\xe0\xb8\xa9\xe0\xb8\xb2"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'pat1': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 PAT 1"', 'blank': 'True'}),
            'pat1_date': ('models.ForeignKey', ['GPExamDate'], {'related_name': '"pat1_score_set"', 'null': 'True', 'verbose_name': '"\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x99\xe0\xb8\xaa\xe0\xb8\xad\xe0\xb8\x9a PAT 1"', 'blank': 'True'}),
            'pat3': ('models.IntegerField', [], {'null': 'True', 'verbose_name': '"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99 PAT 3"', 'blank': 'True'}),
            'pat3_date': ('models.ForeignKey', ['GPExamDate'], {'related_name': '"pat3_score_set"', 'null': 'True', 'verbose_name': '"\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x99\xe0\xb8\xaa\xe0\xb8\xad\xe0\xb8\x9a PAT 3"', 'blank': 'True'}),
            'school_city': ('models.CharField', [], {'max_length': '50', 'verbose_name': 'u"\xe0\xb8\xad\xe0\xb8\xb3\xe0\xb9\x80\xe0\xb8\xa0\xe0\xb8\xad/\xe0\xb9\x80\xe0\xb8\x82\xe0\xb8\x95"'}),
            'school_name': ('models.CharField', [], {'max_length': '100', 'verbose_name': 'u"\xe0\xb9\x82\xe0\xb8\xa3\xe0\xb8\x87\xe0\xb9\x80\xe0\xb8\xa3\xe0\xb8\xb5\xe0\xb8\xa2\xe0\xb8\x99"'}),
            'school_province': ('models.CharField', [], {'max_length': '25', 'verbose_name': 'u"\xe0\xb8\x88\xe0\xb8\xb1\xe0\xb8\x87\xe0\xb8\xab\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x94"'}),
            'uses_gat_score': ('models.BooleanField', [], {'verbose_name': 'u"\xe0\xb8\x84\xe0\xb8\xb0\xe0\xb9\x81\xe0\xb8\x99\xe0\xb8\x99\xe0\xb8\x97\xe0\xb8\xb5\xe0\xb9\x88\xe0\xb9\x83\xe0\xb8\x8a\xe0\xb9\x89\xe0\xb8\xaa\xe0\xb8\xa1\xe0\xb8\xb1\xe0\xb8\x84\xe0\xb8\xa3"'})
        },
        'application.majorpreference': {
            'applicant': ('models.OneToOneField', ['Applicant'], {'related_name': '"preference"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'majors': ('IntegerListField', [], {})
        },
        'application.major': {
            'Meta': {'ordering': "['number']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'}),
            'number': ('models.CharField', [], {'max_length': '5'})
        },
        'application.applicant': {
            'birth_date': ('models.DateField', [], {'verbose_name': '"\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\x99\xe0\xb9\x80\xe0\xb8\x81\xe0\xb8\xb4\xe0\xb8\x94"'}),
            'email': ('models.EmailField', [], {}),
            'ethnicity': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb9\x80\xe0\xb8\x8a\xe0\xb8\xb7\xe0\xb9\x89\xe0\xb8\xad\xe0\xb8\x8a\xe0\xb8\xb2\xe0\xb8\x95\xe0\xb8\xb4"'}),
            'first_name': ('models.CharField', [], {'max_length': '200', 'verbose_name': '"\xe0\xb8\x8a\xe0\xb8\xb7\xe0\xb9\x88\xe0\xb8\xad"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('models.CharField', [], {'max_length': '300', 'verbose_name': '"\xe0\xb8\x99\xe0\xb8\xb2\xe0\xb8\xa1\xe0\xb8\xaa\xe0\xb8\x81\xe0\xb8\xb8\xe0\xb8\xa5"'}),
            'national_id': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb9\x80\xe0\xb8\xa5\xe0\xb8\x82\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb8\x88\xe0\xb8\xb3\xe0\xb8\x95\xe0\xb8\xb1\xe0\xb8\xa7\xe0\xb8\x9b\xe0\xb8\xa3\xe0\xb8\xb0\xe0\xb8\x8a\xe0\xb8\xb2\xe0\xb8\x8a\xe0\xb8\x99"'}),
            'nationality': ('models.CharField', [], {'max_length': '50', 'verbose_name': '"\xe0\xb8\xaa\xe0\xb8\xb1\xe0\xb8\x8d\xe0\xb8\x8a\xe0\xb8\xb2\xe0\xb8\x95\xe0\xb8\xb4"'}),
            'phone_number': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb8\xab\xe0\xb8\xa1\xe0\xb8\xb2\xe0\xb8\xa2\xe0\xb9\x80\xe0\xb8\xa5\xe0\xb8\x82\xe0\xb9\x82\xe0\xb8\x97\xe0\xb8\xa3\xe0\xb8\xa8\xe0\xb8\xb1\xe0\xb8\x9e\xe0\xb8\x97\xe0\xb9\x8c"'})
        },
        'application.gpexamdate': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'month_year': ('models.CharField', [], {'max_length': '20', 'verbose_name': '"\xe0\xb9\x80\xe0\xb8\x94\xe0\xb8\xb7\xe0\xb8\xad\xe0\xb8\x99\xe0\xb9\x81\xe0\xb8\xa5\xe0\xb8\xb0\xe0\xb8\x9b\xe0\xb8\xb5\xe0\xb8\x82\xe0\xb8\xad\xe0\xb8\x87\xe0\xb8\x81\xe0\xb8\xb2\xe0\xb8\xa3\xe0\xb8\xaa\xe0\xb8\xad\xe0\xb8\x9a"'})
        },
        'application.applicantaccount': {
            'applicant': ('models.OneToOneField', ['Applicant'], {}),
            'hashed_password': ('models.CharField', [], {'max_length': '100'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['application']
