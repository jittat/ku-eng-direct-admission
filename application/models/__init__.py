# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date

from django.db import models
from django.conf import settings

from commons.utils import random_string
from commons.local import PROVINCE_CHOICES, APP_TITLE_CHOICES
from application.fields import IntegerListField

class Applicant(models.Model):

    # core applicant information
    title = models.CharField(max_length=10,
                             choices=APP_TITLE_CHOICES,
                             verbose_name="คำนำหน้า")
    first_name = models.CharField(max_length=200,
                                  verbose_name="ชื่อ")
    last_name = models.CharField(max_length=300,
                                 verbose_name="นามสกุล")
    email = models.EmailField(unique=True)
    hashed_password = models.CharField(max_length=100)

    has_logged_in = models.BooleanField(default=False)
    activation_required = models.BooleanField(default=False)

    # application data

    is_submitted = models.BooleanField(default=False)

    UNDECIDED_METHOD = 0
    SUBMITTED_BY_MAIL = 1
    SUBMITTED_ONLINE = 2
    SUBMITTED_OFFLINE = 3
    SUBMISSION_METHOD_CHOICES = [(UNDECIDED_METHOD,'ยังไม่ได้เลือก'),
                                 (SUBMITTED_BY_MAIL,'ส่งทางไปรษณีย์'),
                                 (SUBMITTED_ONLINE,'ส่งออนไลน์'),
                                 (SUBMITTED_OFFLINE,'ส่งใบสมัครและหลักฐานทางไปรษณีย์')]

    doc_submission_method = models.IntegerField(
        choices=SUBMISSION_METHOD_CHOICES,
        default=UNDECIDED_METHOD)

    is_offline = models.BooleanField(default=False)

    # for related model cache

    RELATED_MODELS = {
        'personal_info': 0,
        'address': 1,
        'educational_info': 2,
        'major_preference': 3,
        'appdocs': 4
        }

    has_related_model = IntegerListField(default=None)

    def check_related_model(self, model_name):
        model_id = Applicant.RELATED_MODELS[model_name]
        if model_id < len(self.has_related_model):
            return (self.has_related_model[model_id] == 1)
        else:
            return None

    def initialize_related_model(self):
        self.has_related_model = [0 
                                  for i in 
                                  range(len(Applicant.RELATED_MODELS))]

    def add_related_model(self, model_name, save=False, smart=False):
        if len(self.has_related_model)==0:
            self.initialize_related_model()
        model_id = Applicant.RELATED_MODELS[model_name]
        old = self.has_related_model[model_id]
        self.has_related_model[model_id] = 1
        if save:
            if (not smart) or (old != 1):
                self.save()
            

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

    @staticmethod
    def get_active_offline_applicant():
        return Applicant.objects.filter(is_offline=True).filter(is_submitted=False)

    # accessor methods

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return "%s %s %s" % (self.title, self.first_name, self.last_name)

    def get_email(self):
        if not self.is_offline:
            return self.email
        else:
            idx = self.email.find('-')
            if idx!=-1:
                return self.email[(idx+1):]
            else:
                return self.email

    def has_personal_info(self):
        result = self.check_related_model('personal_info')
        if result!=None:
            return result
        else:
            try:
                return self.personal_info != None
            except PersonalInfo.DoesNotExist:
                return False

    def get_personal_info_or_none(self):
        if self.has_personal_info():
            return self.personal_info
        else:
            return None

    def has_address(self):
        result = self.check_related_model('address')
        if result!=None:
            return result
        else:
            try:
                return self.address != None
            except ApplicantAddress.DoesNotExist:
                return False            

    def has_educational_info(self):
        result = self.check_related_model('educational_info')
        if result!=None:
            return result
        else:
            try:
                return self.education != None
            except Education.DoesNotExist:
                return False            

    def get_educational_info_or_none(self):
        if self.has_educational_info():
            edu = self.education
            edu.fix_boolean_fields()
            return edu
        else:
            return None

    def has_major_preference(self):
        result = self.check_related_model('major_preference')
        if result!=None:
            return result
        else:
            try:
                return self.preference != None
            except MajorPreference.DoesNotExist:
                return False

    def get_applicant_docs_or_none(self):
        result = self.check_related_model('appdocs')
        if (result!=None) and (result==0):
            return None
        try:
            docs = self.appdocs
        except Exception:
            docs = None
        return docs

    def has_online_docs(self):
        return self.get_applicant_docs_or_none()!=None

    def can_choose_major(self):
        return (self.has_educational_info() and 
                not self.education.uses_anet_score)

    def online_doc_submission(self):
        return self.doc_submission_method == Applicant.SUBMITTED_ONLINE

    def can_resubmit_online_doc(self):
        return (self.online_doc_submission() and
                self.submission_info.is_doc_needs_resubmission())


    ######################
    # methods for authentication

    def set_password(self, passwd):
        import random
        import hashlib

        salt = hashlib.sha1(str(random.random())[2:4]).hexdigest()

        full_password = (salt + '$' +
                         hashlib.sha1(salt + passwd).hexdigest())
        
        self.hashed_password = full_password


    def random_password(self, length=5):
        import random
        password = random_string(5)
        self.set_password(password)
        return password

    def check_password(self, password):
        import hashlib

        salt, enc_passwd = self.hashed_password.split('$')

        try:
            return enc_passwd == (hashlib.sha1(salt + password).hexdigest())
        except UnicodeEncodeError:
            return False


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
    
    def submit(self, submission_method, submitted_at=None):
        if self.is_submitted:
            raise Applicant.DuplicateSubmissionError()
        try:
            submission_info = SubmissionInfo(applicant=self)
            submission_info.random_salt()
            if ((submission_method==Applicant.SUBMITTED_ONLINE) or
                (submission_method==Applicant.SUBMITTED_OFFLINE)):
                submission_info.doc_received_at = datetime.now()
            submission_info.save()
            if submitted_at!=None:
                submission_info.submitted_at = submitted_at
                submission_info.save()
        except:
            raise Applicant.DuplicateSubmissionError()

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

    submitted_at = models.DateTimeField(auto_now_add=True)
    doc_received_at = models.DateTimeField(blank=True, 
                                           null=True,
                                           default=None)
    has_been_reviewed = models.BooleanField(default=False)
    doc_reviewed_complete = models.BooleanField(default=False)

    doc_reviewed_at = models.DateTimeField(blank=True,
                                           null=True,
                                           default=None)

    @staticmethod
    def find_by_ticket_number(ticket):
        if len(ticket)>8:
            return None
        sub_id = ticket[-5:]
        try:
            sub_id = int(sub_id)
            sub = SubmissionInfo.objects.get(pk=sub_id)
            return sub
        except:
            return None

    def random_salt(self):
        self.salt = random_string(10)

    def has_received_doc(self):
        return self.doc_received_at != None

    def can_update_info(self):
        if self.has_been_reviewed:
            return False
        if datetime.now() >= settings.SUBMISSION_CHANGE_GRACE_PERIOD_END:
            return False
        return True

    def can_be_reviewed(self):
        if datetime.now() >= settings.SUBMISSION_CHANGE_GRACE_PERIOD_END:
            return True
        return (datetime.now() > 
                self.submitted_at + 
                settings.SUBMISSION_CHANGE_GRACE_PERIOD)

    def is_doc_needs_resubmission(self):
        return (self.has_been_reviewed and
                (not self.doc_reviewed_complete))

    def set_doc_received_at_now_if_not(self, save=True):
        if self.doc_received_at==None:
            self.doc_received_at = datetime.now()
            if save:
                self.save()

    def toggle_doc_received_at(self, save=True):
        if self.has_received_doc():
            self.doc_received_at = None
        else:
            self.doc_received_at = datetime.now()
        if save:
            self.save()

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
    phone_number = models.CharField(max_length=35,
                                    verbose_name="หมายเลขโทรศัพท์")

class Address(models.Model):
    number = models.CharField(max_length=20,
                              verbose_name="บ้านเลขที่")
    village_number = models.IntegerField(blank=True, 
                                         null=True,
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
    phone_number = models.CharField(max_length=35,
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

    # This is used for post-identifying potential cross review-update
    # condition.  In that case the document must be manually validated
    # again.
    updated_at = models.DateTimeField(auto_now=True)

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

    @staticmethod
    def major_list_to_major_rank_list(major_list):
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
        for m in major_list:
            ranks[rev[m]] = r
            r += 1

        return ranks
        

    def to_major_rank_list(self):
        return MajorPreference.major_list_to_major_rank_list(self.majors)

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
    activation_key = models.CharField(max_length=10, blank=True, unique=True)

    def random_activation_key(self):
        self.activation_key = random_string(10)
        return self.activation_key

    def random_and_save(self):
        success = False
        trials = 0
        while not success:
            try:
                self.random_activation_key()
                self.save()
                success = True
            except:
                trials += 1
                if trials > 10:
                    raise

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
        if not self.last_request_at:
            return False
        today = date.today()
        today_datetime = datetime(today.year, today.month, today.day)
        return self.last_request_at >= today_datetime

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

