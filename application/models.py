# -*- coding: utf-8 -*-

from django.db import models

class Applicant(models.Model):
    first_name = models.CharField(max_length=200,
                                  verbose_name="ชื่อ")
    last_name = models.CharField(max_length=300,
                                 verbose_name="นามสกุล")
    national_id = models.CharField(max_length=20,
                                   verbose_name="เลขประจำตัวประชาชน")
    birth_date = models.DateField(verbose_name="วันเกิด")
    nationality = models.CharField(max_length=50,
                                   verbose_name="สัญชาติ")
    ethnicity = models.CharField(max_length=50,
                                 verbose_name="เชื้อชาติ")
    phone_number = models.CharField(max_length=20,
                                    verbose_name="หมายเลขโทรศัพท์")
    email = models.EmailField()

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def has_address(self):
        try:
            return self.address != None
        except ApplicantAddress.DoesNotExist:
            return False            

    def has_educational_info(self):
        try:
            return self.education != None
        except Education.DoesNotExist:
            return False            

class Address(models.Model):
    number = models.CharField(max_length=20,
                              verbose_name="บ้านเลขที่")
    village_number = models.IntegerField(blank=True,
                                         verbose_name="หมู่ที่")
    village_name = models.CharField(blank=True,
                                    max_length=100,
                                    verbose_name="หมู่บ้าน")
    road = models.CharField(max_length=50,
                            verbose_name="ถนน")
    district = models.CharField(max_length=50,
                                verbose_name="ตำบล/แขวง")
    city = models.CharField(max_length=50,
                            verbose_name="อำเภอ/เขต")
    province = models.CharField(max_length=25,
                                verbose_name="จังหวัด")
    postal_code = models.CharField(max_length=10,
                                   verbose_name="รหัสไปรษณีย์")
    phone_number = models.CharField(max_length=20,
                                    verbose_name="หมายเลขโทรศัพท์")

    def __unicode__(self):
        return ("%s %s %s %s %s %s" % 
                (self.number,
                 self.road,
                 self.district,
                 self.city,
                 self.province,
                 self.postal_code))



class ApplicantAddress(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name="address")
    home_address = models.OneToOneField(Address, 
                                        related_name="home_owner")
    contact_address = models.OneToOneField(Address, 
                                           related_name="contact_owner")

    def __unicode__(self):
        return unicode(self.contact_address)


class Education(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name="education")

    uses_anet_score = models.BooleanField(
        verbose_name="สมัครโดยใช้คะแนน A-NET")
    has_graduated = models.BooleanField(
        verbose_name="จบการศึกษาระดับมัธยมศึกษาปีที่ 6")
    school_name = models.CharField(max_length=100,
                              verbose_name="โรงเรียน")
    school_district = models.CharField(max_length=50, blank=True,
                                       verbose_name="ตำบล/แขวง")
    school_city = models.CharField(max_length=50,
                                   verbose_name="อำเภอ/เขต")
    school_province = models.CharField(max_length=25,
                                       verbose_name="จังหวัด")
    school_postal_code = models.CharField(max_length=10, blank=True,
                                          verbose_name="รหัสไปรษณีย์")
    school_phone_number = models.CharField(max_length=20, blank=True,
                                           verbose_name="หมายเลขโทรศัพท์")
    
    gpax = models.FloatField(verbose_name="GPAX")
    gat = models.IntegerField(blank=True,
                              verbose_name="คะแนน GAT")
    gat_date = models.DateField(blank=True,
                                verbose_name="วันสอบ GAT")
    pat1 = models.IntegerField(blank=True,
                               verbose_name="คะแนน PAT 1")
    pat1_date = models.DateField(blank=True,
                                 verbose_name="วันสอบ PAT 1")
    pat3 = models.IntegerField(blank=True,
                               verbose_name="คะแนน PAT 3")
    pat3_date = models.DateField(blank=True,
                                 verbose_name="วันสอบ PAT 3")
    anet = models.IntegerField(blank=True,
                               verbose_name="คะแนน A-NET")

    def __unicode__(self):
        if self.has_graduated:
            return "จบการศึกษาจากโรงเรียน" + self.school_name
        else:
            return "กำลังศึกษาอยู่ที่โรงเรียน" + self.school_name

