# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

from django.db import models
from django.conf import settings

from commons.utils import random_string
from commons.utils import PROVINCE_CHOICES
from application.fields import IntegerListField


class Applicant(models.Model):

    # core applicant information
    first_name = models.CharField(max_length=200,
                                  verbose_name="ชื่อ")
    last_name = models.CharField(max_length=300,
                                 verbose_name="นามสกุล")
    email = models.EmailField(unique=True)
    hashed_password = models.CharField(max_length=100)

    has_logged_in = models.BooleanField(default=False)
    activation_required = models.BooleanField(default=False)

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


    class DuplicateSubmissionError(Exception):
        pass

    ###################
    # class accessor methods

    @staticmethod
    def get_applicant_by_email(email):
        applicants = Applicant.objects.filter(email=email).all()
        if len(applicants)==0:
            return None
        else:
            return applicants[0]

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

    def online_doc_submission(self):
        return self.doc_submission_method == Applicant.SUBMITTED_ONLINE

    ######################
    # methods for authentication

    def set_password(self, passwd):
        import random
        import hashlib

        salt = hashlib.sha1(str(random.random())[2:4]).hexdigest()

        full_password = (salt + '$' +
                         hashlib.sha1(salt + passwd).hexdigest())
        
        self.hashed_password = full_password


    def random_password(self):
        import random
        password = random_string(5)
        self.set_password(password)
        return password

    def check_password(self, password):
        import hashlib

        salt, enc_passwd = self.hashed_password.split('$')

        return enc_passwd == (hashlib.sha1(salt + password).hexdigest())


    def can_request_password(self):
        """
        checks if a user can request a new password, and saves the
        request log.  The criteria are:

        - the user hasn't requested the new password within 5 minutes,
        - the user hasn't requested the new password more than
        settings.MAX_PASSWORD_REQUST_PER_DAY (set in settings.py)
        times.
        """
        # get the log
        try:
            request_log = self.password_request_log
        except PasswordRequestLog.DoesNotExist:
            request_log = None
        
        if request_log==None:
            # request for the first time
            request_log = PasswordRequestLog.create_for(self)
            request_log.save()
            return True

        result = True
        if (request_log.last_request_at >= 
            datetime.now() - timedelta(minutes=5)):
            result = False

        if (request_log.requested_today() and
            request_log.num_requested_today >=
            settings.MAX_PASSWORD_REQUST_PER_DAY):
            result = False

        request_log.update()
        request_log.save()
        return result

    def verify_activation_key(self, key):
        for reg in self.registrations.all():
            if key==reg.activation_key:
                return True
        return False

    ######################
    # tickets

    def generate_submission_ticket(self):
        pass

    def ticket_number(self):
        application_id = self.submission_info.applicantion_id
        return ("%(year)d%(method)d%(id)05d" % 
                { 'year': settings.ADMISSION_YEAR,
                  'method': self.doc_submission_method,
                  'id': application_id })

    def verification_number(self):
        key = u"%s-%s-%s-%s" % (
            self.submission_info.salt,
            self.email,
            self.first_name,
            self.last_name)
        import hashlib
        h = hashlib.md5()
        h.update(key.encode('utf-8'))
        return h.hexdigest()


    #######################
    # submission
    
    def submit(self, submission_method):
        if self.is_submitted:
            raise Applicant.DuplicateSubmissionError()
        submission_info = SubmissionInfo(applicant=self)
        submission_info.random_salt()
        submission_info.save()
        self.doc_submission_method = submission_method
        self.is_submitted = True
        self.save()


class SubmissionInfo(models.Model):
    """
    associates Applicant who have submitted the applicaiton with a
    unique applicantion_id.
    """
    applicantion_id = models.AutoField(unique=True, primary_key=True)
    applicant = models.OneToOneField(Applicant, 
                                     related_name="submission_info")
    salt = models.CharField(max_length=30)

    def random_salt(self):
        self.salt = random_string(10)

    class Meta:
        ordering = ['applicantion_id']


class PersonalInfo(models.Model):
    applicant = models.OneToOneField(Applicant, related_name="personal_info")
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
    road = models.CharField(blank=True, null=True, 
                            max_length=50,
                            verbose_name="ถนน")
    district = models.CharField(max_length=50,
                                verbose_name="ตำบล/แขวง")
    city = models.CharField(max_length=50,
                            verbose_name="อำเภอ/เขต")
    province = models.CharField(max_length=25,
                                choices=PROVINCE_CHOICES,
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
                                       choices=PROVINCE_CHOICES,
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


####################################################
# models for registration data
#

class Registration(models.Model):
    applicant = models.ForeignKey(Applicant,related_name="registrations")
    registered_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=300)
    activation_key = models.CharField(max_length=10, blank=True)

    def random_activation_key(self):
        self.activation_key = random_string(10)

    class Meta:
        ordering = ['-registered_at']


class PasswordRequestLog(models.Model):
    """
    keeps track of password requests.  It is used when calling to
    Applicant.can_request_password()
    """
    applicant = models.OneToOneField(Applicant,related_name='password_request_log')
    last_request_at = models.DateTimeField()
    num_requested_today = models.IntegerField(default=0)

    @staticmethod
    def create_for(applicant):
        log = PasswordRequestLog(applicant=applicant,
                                 last_request_at=datetime.now(),
                                 num_requested_today=1)
        return log

    def requested_today(self):
        return self.last_request_at >= datetime.today()

    def update(self):
        """
        updates the number of requests for today, and the requested
        timestamp.
        """
        self.last_request_at = datetime.now()
        if self.requested_today():
            self.num_requested_today = self.num_requested_today + 1
        else:
            self.num_requested_today = 1
