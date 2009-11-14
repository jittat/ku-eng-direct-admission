# -*- coding: utf-8 -*-
from django.conf import settings
from commons.utils import admin_email
from django.core.urlresolvers import reverse

# favour django-mailer but fall back to django.core.mail
try:
    if (("mailer" in settings.INSTALLED_APPS) and 
        settings.SEND_MAILS_THROUGH_DJANGO_MAILER):
        from mailer import send_mail
    else:
        from django.core.mail import send_mail
except:
    from django.core.mail import send_mail
    

def adm_send_mail(to_email, subject, message, force=False):
    sender = admin_email()

    send_real_email = True

    try:
        if settings.FAKE_SENDING_EMAIL:
            send_real_email = False
    except:
        pass
    
    if send_real_email:
        send_mail(subject,
                  message,
                  sender,
                  [ to_email ],
                  fail_silently=True)
    else:
        print 'Does not send email'
        print 'Message:'
        print message


def send_password_by_email(applicant, password, force=False):
    """
    sends password to applicant.
    """
    subject = 'รหัสผ่านสำหรับการสมัครเข้าศึกษาแบบทางตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

ขอบคุณที่ได้ลงทะเบียนเพื่อสมัครเข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ บางเขน

รหัสผ่านของคุณคือ %(password)s

คุณสามารถเข้าใช้ระบบได้โดยป้อนอีเมล์นี้ (%(email)s) และป้อนรหัสผ่านด้านบน

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ กรุณาช่วยแจ้งผู้ดูแล้วด้วย

-โครงการรับสมัครตรง
"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.email, 
    'password': password }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.email, subject, message, force)


def send_activation_by_email(applicant, activation_key, force=False):
    """
    sends activation key to an email.
    """

    base_path = settings.HTTP_BASE_PATH
    subject = 'รหัสสำหรับเปิดใช้งานบัญชีผู้ใช้สำหรับการสมัครเข้าศึกษาต่อคณะวิศวกรรมศาสตร์ มก.บางเขน'
    message = (
u"""เรียน คุณ %(firstname)s %(lastname)s

เราขอส่งรหัสสำหรับยืนยันอีเมล์เพื่อสำหรับบัญชีผู้ใช้ของระบบรับสมัครเข้าศึกษาต่อของคณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน

กรุณากดลิงก์ต่อไปนี้ <a href="%(link)s">%(link)s</a> เพื่อยืนยันบัญชีที่คุณได้ลงทะเบียนไว้

เมื่อยืนยันเรียบร้อยแล้ว เราจะส่งรหัสผ่านมายังอีเมล์นี้อีกครั้งหนึ่ง

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ กรุณาช่วยแจ้งผู้ดูแล้วด้วย

-โครงการรับสมัครตรง
"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.email, 
    'link': base_path + reverse('apply-activate', 
                                args=[activation_key]) }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.email, subject, message, force)


def send_submission_confirmation_by_email(applicant, force=False):
    """
    sends submission confirmation
    """
    subject = 'ยืนยันการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    if applicant.online_doc_submission():
        greeting = u"จดหมายอิเล็กทรอนิกส์ฉบับนี้ ยืนยันว่าคณะวิศวกรรมศาสตร์ได้รับใบสมัครของคุณแล้ว โดยคุณได้อัพโหลดหลักฐานทั้งหมดทางออนไลน์ อย่างไรก็ตามหลักฐานทั้งหมดจะต้องผ่านการตรวจสอบความถูกต้องเสียก่อนการสมัครจึงเสร็จสิ้นสมบูรณ์"
    else:
        greeting = u"จดหมายอิเล็กทรอนิกส์ฉบับนี้ ยืนยันว่าคณะวิศวกรรมศาสตร์ได้รับข้อมูลพื้นฐานในการสมัครของคุณแล้ว อย่างไรก็ตามคุณเลือกที่จะส่งหลักฐานทางไปรษณีย์ ดังนั้นการสมัครจะสมบูรณ์ก็ต่อเมื่อทางคณะได้รับหลักฐานและตรวจสอบแล้ว"

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

%(greeting)s

เลขประจำตัวผู้สมัครที่คุณได้รับคือ %(ticket)s
รหัสยืนยันคือ %(verification)s
โดยการสมัครได้สมัครโดยใช้อีเมล์ %(email)s

คุณสามารถเข้าสู่ระบบรับสมัครเพื่อตรวจสอบสถานะใบสมัครได้โดยใช้อีเมล์ %(email)s 

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'greeting': greeting,
    'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.email, 
    'ticket': applicant.ticket_number(),
    'verification': applicant.verification_number(),
    'submission_method': applicant.get_doc_submission_method_display(),
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.email, subject, message, force)

