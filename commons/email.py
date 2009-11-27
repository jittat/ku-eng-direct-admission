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

    if settings.EMAIL_SENDER=='':
        sender = admin_email()
    else:
        sender = settings.EMAIL_SENDER

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
u"""เรียนคุณ %(firstname)s %(lastname)s<br/>
<br/>
ขอบคุณที่ได้ลงทะเบียนเพื่อสมัครเข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ บางเขน<br/>
<pre>

รหัสผ่านของคุณคือ %(password)s

</pre>
คุณสามารถเข้าใช้ระบบได้โดยป้อนอีเมล์นี้ (%(email)s) และป้อนรหัสผ่านด้านบน<br/>
<br/>
ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ กรุณาช่วยแจ้งผู้ดูแล้วด้วย</br>
<br/>
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

    base_path = settings.HTTP_BASE_PATH
    subject = 'รหัสสำหรับเปิดใช้งานบัญชีผู้ใช้สำหรับการสมัครเข้าศึกษาต่อคณะวิศวกรรมศาสตร์ มก.บางเขน'
    message = (
u"""เรียน คุณ %(firstname)s %(lastname)s

เราขอส่งรหัสสำหรับยืนยันอีเมล์เพื่อสำหรับบัญชีผู้ใช้ของระบบรับสมัครเข้าศึกษาต่อของคณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน

กรุณากดลิงก์ต่อไปนี้ <a href="%(link)s">%(link)s</a> เพื่อยืนยันบัญชีที่คุณได้ลงทะเบียนไว้

เมื่อยืนยันเรียบร้อยแล้ว เราจะส่งรหัสผ่านมายังอีเมล์นี้อีกครั้งหนึ่ง

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ กรุณาช่วยแจ้งผู้ดูแลด้วย

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


def send_sub_method_change_notice_by_email(applicant, force=False):
    """
    sends doc submission method change notice
    """
    subject = 'แจ้งการเปลี่ยนแปลงวิธีการส่งหลักฐานเพื่อการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์นี้แจ้งให้คุณทราบว่าคุณได้ยกเลิกการส่งหลักฐานทางไปรษณีย์
และเปลี่ยนไปใช้การส่งหลักฐานแบบออนไลน์

กระบวนการดังกล่าวจะทำให้ผู้สมัครเปลี่ยนสถานะกลับไปเป็น<b>ผู้สมัครที่ยังไม่ได้ยื่นใบสมัคร</b>
และทำให้หมายเลขประจำตัวผู้สมัครหมายเลขเดิมที่ผู้สมัครเคยได้รับถูกยกเลิก
ผู้สมัครจะได้รับหมายเลขประจำตัวใหม่อีกครั้งเมื่อยื่นหลักฐานครบและได้ยืนยันหลักฐานอีกครั้ง

อย่าลืมว่าคุณจะต้องกลับไปยืนยันเอกสารและส่งใบสมัครอีกครั้ง

ถ้าคุณได้รับเมล์นี้ โดยไม่ได้เลือกเปลี่ยนการส่งข้อมูล อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ กรุณาช่วยแจ้งผู้ดูแล้วด้วย

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.email, 
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.email, subject, message, force)


def send_validation_successful_by_email(applicant, force=False):
    """
    sends validation result
    """
    subject = 'การตรวจหลักฐานเพื่อการสมัครตรงเรียบร้อย'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์นี้แจ้งว่าคณะวิศวกรรมศาสตร์ได้ตรวจสอบหลักฐานที่คุณได้ยื่นให้กับคณะ
เพื่อใช้ในการสมัครเข้าศึกษาต่อ ด้วยวิธีรับตรง ประจำปีการศึกษา 2553 แล้ว

หลักฐานที่คุณส่งมานั้นครบถ้วนและสมบูรณ์แล้ว ขณะนี้คุณได้เข้าสู่กระบวนการคัดเลือกของคณะต่อไป
คณะจะประกาศรายชื่อผู้มีสิทธิ์เข้ารับการคัดเลือกเข้าศึกษาต่อแบบรับตรงในวันที่ 22 ธ.ค. 2552

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_validation_error_by_email(applicant, failed_fields, force=False):
    """
    sends validation result
    """

    error_list = []
    for field, result in failed_fields:
        error_list.append('%s - %s' % (field.name, result.applicant_note))
    errors = '\n'.join(error_list)

    extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ภายในวันที่ 15 ธ.ค. นี้  โดยใช้วิธีส่งแบบเดิม
ถ้าคุณใช้การส่งหลักฐานทางไปรษณีย์ อย่าลืมพิมพ์ใบนำส่งแนบมาด้วย (สามารถพิมพ์ได้จากเว็บรับสมัคร)"""
    if applicant.is_offline:
        extra_msg = u"""คุณจะต้องส่งหลักฐาน ภายในวันที่ 15 ธ.ค. นี้
เนื่องจากคุณสมัครโดยส่งใบสมัครและหลักฐานทุกอย่างทางไปรษณีย์ 
ในการส่งหลักฐานให้ระบุให้ชัดเจนว่าเป็นการส่งหลักฐานเพิ่มเติม
และให้ระบุหมายเลขประจำตัวผู้สมัครว่า %(ticket_number)s ด้วย""" % {'ticket_number': applicant.ticket_number()}

    subject = 'การตรวจหลักฐานเพื่อการสมัครตรงไม่ผ่าน'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์นี้แจ้งว่าคณะวิศวกรรมศาสตร์ได้ตรวจสอบหลักฐานที่คุณได้ยื่นให้กับคณะ
เพื่อใช้ในการสมัครเข้าศึกษาต่อ ด้วยวิธีรับตรง ประจำปีการศึกษา 2553 แล้ว

หลักฐานที่คุณส่งมานั้นมีปัญหาดังนี้:
%(errors)s

%(extra_msg)s

ถ้ามีข้อสงสัยประการใด สามารถสอบถามได้ในเว็บบอร์ด หรือส่งเมล์หาผู้ดูแลที่ %(admin_email)s

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'errors': errors,
    'extra_msg': extra_msg,
    'admin_email': admin_email()
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)

