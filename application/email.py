# -*- encoding: utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from commons.utils import admin_email
from django.core.urlresolvers import reverse

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
)
    adm_send_mail(applicant.email, subject, message, force)


def send_activation_by_email(applicant, activation_key, force=False):
    """
    sends activation key to an email.
    """
    subject = 'รหัสสำหรับเปิดใช้งานบัญชีผู้ใช้สำหรับการสมัครเข้าศึกษาต่อคณะวิศวกรรมศาสตร์ มก.บางเขน'
    message = (
u"""Dear %(firstname)s %(lastname)s

Thank you for applying at the Faculty of Engineering, Kasetsart University.

Click this link to activate your account: 
<a href="%(link)s">%(link)s</a>

Use your e-mail address (%(email)s) to log in.

Thank you.
-jittat"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.email, 
    'link': reverse('apply-activate', 
                    args=[applicant.id, activation_key]) }
)
    adm_send_mail(applicant.email, subject, message, force)
