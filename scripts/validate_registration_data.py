# -*- coding: utf-8 -*-
import sys
import codecs

if len(sys.argv)<2:
    print "Usage: validate.py [round_number_for_result] [--email]"
    quit()

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import AdmissionResult
from confirmation.models import AdmissionConfirmation, StudentRegistration
from application.models import Applicant
from commons.email import adm_send_mail

def validate(applicant):
    try:
        reg = applicant.student_registration
    except StudentRegistration.DoesNotExist:
        reg = None


    msg = ''
    if reg==None:
        msg = u'ไม่ได้กรอกข้อมูล'
    else:
        errors = []
        if not reg.validate(errors):
            msg = u'ข้อมูลไม่ครบ: ' + ' '.join(errors)

    if msg != '':
        print u'"%s","%s","%s","%s"' % (applicant.national_id,
                                   applicant.full_name(),
                                   applicant.personal_info.phone_number,
                                   msg)
    return msg == ''


def send_reminder(email):
    subject = u'[รับตรงวิศวกรรมศาสตร์ มก.] กรอกข้อมูลขึ้นทะเบียนนิสิตใหม่ ภายในวันที่ 17 ก.พ.'
    message = u'''เรียน ผู้ได้รับคัดเลือกโครงการรับตรงปีการศึกษา 2554

ทางโครงการได้ตรวจสอบแล้ว คุณยังไม่ได้กรอกข้อมูล (หรือกรอกข้อมูลไม่ครบ) สำหรับขึ้นทะเบียนเป็นนิสิตใหม่
ถ้าเราได้ข้อมูลไม่ครบถ้วน โครงการจะไม่สามารถรับคุณเข้าเป็นนิสิตใหม่ได้

ดังนั้นให้คุณรีบเข้ามากรอกข้อมูล ผ่านทางระบบรับสมัครออนไลน์ ภายในเวลา 23:59 น.ของวันที่ 17 ก.พ. 2554 ไม่เช่นนั้นคุณอาจไม่มีสิทธิ์เข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์

ถ้ามีข้อสงสัยประการใดสามารถสอบถามได้ทางโทรศัพท์ หรือทางอีเมล์ admission.eng.ku@gmailcom
'''
    adm_send_mail(email, subject, message)


def main():
    round_number = sys.argv[1]
    is_send_email = (len(sys.argv)==3) and (sys.argv[2]=='--email')
    counter = 0
    for res in AdmissionResult.objects.filter(round_number=round_number).all():
        a = res.applicant

        paid_total = sum([c.paid_amount for c in a.admission_confirmations.all()])
        confirmed = paid_total >= res.admitted_major.confirmation_amount

        if confirmed:
            if not validate(a):

                if is_send_email:
                    send_reminder(a.email)

                counter += 1

    print "Total:", counter

if __name__=='__main__':
    main()
