# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from fields import IntegerListField

class Applicant(models.Model):
    # core applicant information
    first_name = models.CharField(max_length=200,
                                  verbose_name="ชื่อ")
    last_name = models.CharField(max_length=300,
                                 verbose_name="นามสกุล")
    email = models.EmailField()
    hashed_password = models.CharField(max_length=100)

    # application data

    UNDECIDED_METHOD = 0
    SUBMITTED_BY_MAIL = 1
    SUBMITTED_ONLINE = 2
    SUBMISSION_METHOD_CHOICES = [(UNDECIDED_METHOD,'ยังไม่ได้เลือก'),
                                 (SUBMITTED_BY_MAIL,'ส่งทางไปรษณีย์'),
                                 (SUBMITTED_ONLINE,'ส่งออนไลน์')]

    is_submitted = models.BooleanField(default=False)
    doc_submission_method = models.IntegerField(
        choices=SUBMISSION_METHOD_CHOICES,
        default=UNDECIDED_METHOD)

    # accessor methods

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def has_personal_info(self):
        try:
            return self.personal_info != None
        except PersonalInfo.DoesNotExist:
            return False

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

    def has_major_preference(self):
        try:
            return self.preference != None
        except MajorPreference.DoesNotExist:
            return False

    def can_choose_major(self):
        return (self.has_educational_info() and 
                not self.education.uses_anet_score)

    # methods for authentication

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
            [random.choice(Applicant.PASSWORD_CHARS) 
             for t in range(5)])

        self.set_password(password)
        return password

    def check_password(self, password):
        import hashlib

        salt, enc_passwd = self.hashed_password.split('$')

        return enc_passwd == (hashlib.sha1(salt + password).hexdigest())
    

    # tickets

    def generate_submission_ticket(self):
        pass

    def ticket_number(self):
        return ("%(year)d%(method)d%(id)05d" % 
                { 'year': settings.ADMISSION_YEAR,
                  'method': self.doc_submission_method,
                  'id': self.id })

    def verification_number(self):
        return "12345678901234567890"


class PersonalInfo(models.Model):
    applicant = models.OneToOneField(Applicant,related_name="personal_info")
    national_id = models.CharField(max_length=20,
                                   verbose_name="เลขประจำตัวประชาชน")
    birth_date = models.DateField(verbose_name="วันเกิด")
    nationality = models.CharField(max_length=50,
                                   verbose_name="สัญชาติ")
    ethnicity = models.CharField(max_length=50,
                                 verbose_name="เชื้อชาติ")
    phone_number = models.CharField(max_length=20,
                                    verbose_name="หมายเลขโทรศัพท์")

class Address(models.Model):
    number = models.CharField(max_length=20,
                              verbose_name="บ้านเลขที่")
    village_number = models.IntegerField(blank=True, null=True,
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
        choices=((False,u"กำลังเรียนระดับมัธยมศึกษาปีที่ 6"),
                 (True,u"จบการศึกษาระดับมัธยมศึกษาปีที่ 6")),
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
    gat = models.FloatField(blank=True, null=True,
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

    def fix_boolean_fields(self):
        self.has_graduated = bool(self.has_graduated)
        self.uses_gat_score = bool(self.uses_gat_score)

    def __unicode__(self):
        if self.has_graduated:
            return u"จบการศึกษาจากโรงเรียน" + self.school_name
        else:
            return u"กำลังศึกษาอยู่ที่โรงเรียน" + self.school_name


class Major(models.Model):
    number = models.CharField(max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return "%s: %s" % (self.number, self.name)

    def select_id(self):
        return "major_%d" % (self.id,)

    __major_list = None

    @staticmethod
    def get_all_majors():
        if Major.__major_list==None:
            Major.__major_list = list(Major.objects.all())
        return Major.__major_list


class MajorPreference(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name="preference")
    majors = IntegerListField()

    def to_major_rank_list(self):
        """
        return a list of preference ranks for each major
        """
        all_majors = Major.get_all_majors()
        major_count = len(all_majors)

        ranks = [None] * major_count

        rev = {}
        for i in range(major_count):
            rev[int(all_majors[i].number)] = i

        r = 1
        for m in self.majors:
            ranks[rev[m]] = r
            r += 1

        return ranks

    def get_major_list(self):
        """
        return a list of majors ordered by preference
        """
        all_majors = Major.get_all_majors()

        majors_dict = {}
        for m in all_majors:
            majors_dict[int(m.number)] = m

        l = []
        for number in self.majors:
            l.append(majors_dict[number])

        return l

