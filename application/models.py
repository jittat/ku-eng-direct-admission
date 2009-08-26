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

    def can_choose_major(self):
        return (self.has_educational_info() and 
                not self.education.uses_anet_score)


class ApplicantAccount(models.Model):
    applicant = models.ForeignKey(Applicant)
    hashed_password = models.CharField(max_length=100)

    PASSWORD_CHARS = 'abcdefghjkmnopqrstuvwxyz'

    def set_password(self, passwd):
        import random
        import hashlib

        salt = hashlib.sha1(str(random.random())[2:4]).hexdigest()

        full_password = (salt + '$' +
                         hashlib.sha1(salt + passwd).hexdigest())
        
        self.hashed_password = full_password


    def random_password(self):
        import random
        password = ''.join(
            [random.choice(ApplicantAccount.PASSWORD_CHARS) 
             for t in range(5)])

        self.set_password(password)
        return password

    def check_password(self):
        import hashlib

        salt, enc_passwd = self.hashed_password.split('$')

        return enc_passwd == (hashlib.sha1(salt + password).hexdigest())
    


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


class GPExamDate(models.Model):
    month_year = models.CharField(max_length=20,
                                  verbose_name="เดือนและปีของการสอบ")

    def __unicode__(self):
        return self.month_year

class Education(models.Model):

    applicant = models.OneToOneField(Applicant,
                                     related_name="education")

    # school information
    has_graduated = models.BooleanField(
        choices=((True,u"จบการศึกษาระดับมัธยมศึกษาปีที่ 6"),
                (False,u"กำลังเรียนระดับมัธยมศึกษาปีที่ 6")),
        verbose_name=u"ระดับการศึกษา")
    school_name = models.CharField(max_length=100,
                                   verbose_name=u"โรงเรียน")
    school_city = models.CharField(max_length=50,
                                   verbose_name=u"อำเภอ/เขต")
    school_province = models.CharField(max_length=25,
                                       verbose_name=u"จังหวัด")

    # test score
    uses_gat_score = models.BooleanField(
        choices=((True,u"GAT/PAT"),
                (False,u"ANET")),
        verbose_name=u"คะแนนที่ใช้สมัคร")
    gpax = models.FloatField(verbose_name="GPAX")
    gat = models.IntegerField(blank=True, null=True,
                              verbose_name="คะแนน GAT")
    gat_date = models.ForeignKey(GPExamDate,
                                 blank=True, null=True,
                                 verbose_name="วันสอบ GAT",
                                 related_name="gat_score_set")
    pat1 = models.IntegerField(blank=True, null=True,
                               verbose_name="คะแนน PAT 1")
    pat1_date = models.ForeignKey(GPExamDate,
                                  blank=True, null=True,
                                  verbose_name="วันสอบ PAT 1",
                                  related_name="pat1_score_set")
    pat3 = models.IntegerField(blank=True, null=True,
                               verbose_name="คะแนน PAT 3")
    pat3_date = models.ForeignKey(GPExamDate,
                                  blank=True, null=True,
                                  verbose_name="วันสอบ PAT 3",
                                  related_name="pat3_score_set")
    anet = models.IntegerField(blank=True, null=True,
                               verbose_name="คะแนน A-NET")

    def __unicode__(self):
        if self.has_graduated:
            return "จบการศึกษาจากโรงเรียน" + self.school_name
        else:
            return "กำลังศึกษาอยู่ที่โรงเรียน" + self.school_name


class Major(models.Model):
    number = models.CharField(max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return "%s: %s" % (self.number, self.name)
