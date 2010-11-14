# -*- coding: utf-8 -*-
from django.conf import settings
from commons.utils import admin_email, submission_deadline_passed
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
    'email': applicant.get_email(), 
    'password': password }
)
    adm_send_mail(applicant.get_email(), subject, message, force)


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
    'email': applicant.get_email(), 
    'link': base_path + reverse('apply-activate', 
                                args=[activation_key]) }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_submission_confirmation_by_email(applicant, force=False):
    """
    sends submission confirmation
    """
    subject = 'ยืนยันการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    greeting = u"จดหมายอิเล็กทรอนิกส์ฉบับนี้ ยืนยันว่าคณะวิศวกรรมศาสตร์ได้รับใบสมัครของคุณแล้ว"

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

%(greeting)s

หมายเลขประจำตัวประชาชนคือ %(national_id)s
รหัสยืนยันคือ %(verification)s
โดยการสมัครได้สมัครโดยใช้อีเมล์ %(email)s

คุณสามารถเข้าสู่ระบบรับสมัครเพื่อตรวจสอบสถานะใบสมัครได้โดยใช้รหัสประจำตัวประชาชนของคุณ

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'greeting': greeting,
    'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'national_id': applicant.national_id,
    'verification': applicant.verification_number(),
    'submission_method': applicant.get_doc_submission_method_display(),
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_resubmission_confirmation_by_email(applicant, force=False):
    """
    sends submission confirmation
    """
    subject = 'ยืนยันการยื่นหลักฐานเพิ่มเติม การสมัครตรงคณะวิศวกรรมศาสตร์ (รอบ 2) ม.เกษตรศาสตร์ บางเขน'

    greeting = u"จดหมายอิเล็กทรอนิกส์ฉบับนี้ ยืนยันว่าคณะวิศวกรรมศาสตร์ได้รับการยื่นหลักฐานเพิ่มเติมของคุณแล้ว ใบสมัครของคุณจะเข้าสู่กระบวนการตรวจสอบหลักฐานซ้ำอีกครั้ง เมื่อการตรวจเรียบร้อยแล้วคณะจะส่งอีเมล์ยืนยันให้กับคุณอีกครั้ง"

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

%(greeting)s

เลขประจำตัวผู้สมัครของคุณคือ %(ticket)s
รหัสยืนยันคือ %(verification)s
โดยการสมัครได้สมัครโดยใช้อีเมล์ %(email)s

คุณสามารถเข้าสู่ระบบรับสมัครเพื่อตรวจสอบสถานะใบสมัครได้โดยใช้อีเมล์ %(email)s 

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'greeting': greeting,
    'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'ticket': applicant.ticket_number(),
    'verification': applicant.verification_number(),
    'submission_method': applicant.get_doc_submission_method_display(),
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)



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
    'email': applicant.get_email(), 
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_validation_successful_by_email(applicant, force=False):
    """
    sends validation result
    """
    subject = 'การตรวจหลักฐานเพื่อการสมัครตรงเรียบร้อย'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์นี้แจ้งว่าคณะวิศวกรรมศาสตร์ได้ตรวจสอบหลักฐานที่คุณได้ยื่นให้กับคณะ
เพื่อใช้ในการสมัครเข้าศึกษาต่อ ด้วยวิธีรับตรง (รอบ 2) ประจำปีการศึกษา 2553 แล้ว

หลักฐานที่คุณส่งมานั้นครบถ้วนและสมบูรณ์แล้ว ขณะนี้คุณได้เข้าสู่กระบวนการคัดเลือกของคณะต่อไป
คณะจะประกาศรายชื่อผู้ได้รับการคัดเลือกเข้าศึกษาต่อแบบรับตรง (รอบ 2) ในวันที่ 11 พ.ค. 2553

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

    if applicant.is_offline:
        extra_msg = u"""คุณจะต้องส่งหลักฐาน ภายในวันที่ 15 ธ.ค. นี้
เนื่องจากคุณสมัครโดยส่งใบสมัครและหลักฐานทุกอย่างทางไปรษณีย์ 
ในการส่งหลักฐานให้ระบุให้ชัดเจนว่าเป็นการส่งหลักฐานเพิ่มเติม
และให้ระบุหมายเลขประจำตัวผู้สมัครว่า %(ticket_number)s ด้วย""" % {'ticket_number': applicant.ticket_number()}
    elif applicant.online_doc_submission():
#        extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ภายในวันที่ 15 ธ.ค. นี้  โดยใช้วิธีส่งแบบออนไลน์เช่นเดิม"""
        extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ภายในวันที่ 9 พ.ค. นี้  โดยใช้วิธีส่งแบบออนไลน์เช่นเดิม"""
    else:
        extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ผ่านทางระบบออนไลน์ ภายในวันที่ 9 พ.ค. 2553 นี้"""
#        extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ภายในวันที่ 15 ธ.ค. นี้  โดยใช้วิธีส่งทางไปรษณีย์เช่นเดิม
#ถ้าคุณใช้การส่งหลักฐานทางไปรษณีย์ อย่าลืมพิมพ์ใบนำส่งแนบมาด้วย (สามารถพิมพ์ได้จากเว็บรับสมัคร)"""

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


def send_resubmission_reminder_by_email(applicant, force=False):
    """
    sends resubmission reminder result
    """

    subject = 'การส่งหลักฐานเพิ่มเติมในการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายฉบับนี้ส่งมาเพื่อเตือนว่าใบสมัครเข้าศึกษาต่อแบบรับตรง
ที่คุณส่งให้กับทางคณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน
มีหลักฐานบางอย่างที่ไม่ผ่านการตรวจ

ถ้าคุณได้ส่งหลักฐานมาใหม่แล้ว เราต้องขออภัยที่แจ้งซ้ำซ้อน

ถ้าคุณต้องการส่งหลักฐานเพิ่มเติมในขณะนี้ 
ยังสามารถทำได้แต่ต้องส่งหลักฐานเพิ่มแบบออนไลน์เท่านั้น
โดยเข้าไปที่เว็บไซต์รับตรง http://admission.eng.ku.ac.th/adm/
เข้าใช้ระบบแล้วเลือก "ส่งหลักฐานเพิ่มเติม" ปุ่มสีน้ำเงินด้านขวา
ระบบนี้จะเปิดให้ส่งได้ถึงวันที่ 9 พ.ค. นี้เท่านั้น

หลักฐานที่ส่งแบบออนไลน์นั้นสามารถนำเข้าเครื่อง
โดยใช้การสแกนหรือการถ่ายรูปด้วยกล้องดิจิทัลก็ได้ 
(ดูรายละเอียดเกี่ยวกับความละเอียดในจากหน้าเว็บ)

ถ้ามีข้อสงสัยประการใด สามารถสอบถามได้ในเว็บบอร์ด 
หรือส่งเมล์หาผู้ดูแลที่ %(admin_email)s

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'admin_email': admin_email()
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_status_by_email_no_applicant(email, force=False):
    subject = 'สถานะการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'
    message = (
u"""เรียนผู้ใช้อีเมล์ %(email)s

ไม่พบข้อมูลการสมัครเข้าศึกษาแบบรับตรง ประจำปีการศึกษา 2553 
ที่คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตบางเขน

ถ้าคุณได้ส่งสมัครมาที่คณะ อาจเป็นไปได้ที่จดหมายยังไม่ถึง
หรือมีการกรอกข้อมูลอีเมล์ผิดพลาด  ให้รีบติดต่อที่ %(admin_email)s โดยด่วน 
พร้อมทั้งระบุชื่อ นามสกุล และหมายเลขประจำตัวประชาชน 
เพื่อให้ทางทีมงานตรวจสอบ

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'email': email,
    'admin_email': admin_email() }
).replace('\n','<br/>\n')
    adm_send_mail(email, subject, message, force)


def send_status_by_email_not_submitted(email, applicants, force=False):
    subject = 'สถานะการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    applicant_names = '\n'.join([a.full_name() for a in applicants])

    message = (
u"""เรียนผู้ใช้อีเมล์ %(email)s

จากการตรวจสอบพบผู้ลงทะเบียนด้วยอีเมล์นี้ แต่ไม่มีข้อมูลการยืนยันใบสมัคร

โดยข้อมูลผู้ลงทะเบียนโดยใช้อีเมล์นี้มีรายชื่อดังนี้

%(applicant_names)s

เนื่องจากใบสมัครที่ส่งยังไม่ได้รับการยืนยัน ทางคณะจึงยังไม่ได้ประมวลผลใบสมัครของคุณ
ถ้าคุณต้องการยืนยันการสมัคร ให้รีบติดต่อผู้ดูทางอีเมล์ %(admin_email)s 
เพื่อให้ยืนยันและตรวจสอบหลักฐานโดยด่วน

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'email': email,
    'applicant_names': applicant_names,
    'admin_email': admin_email() }
).replace('\n','<br/>\n')
    adm_send_mail(email, subject, message, force)


def summarize_applicant_status(applicant):
    if applicant.is_submitted:
        ticket_number = applicant.ticket_number()
        submission_status = u"สถานะใบสมัคร: ยืนยันแล้ว"
        if applicant.submission_info.has_been_reviewed:
            if applicant.submission_info.doc_reviewed_complete:
                review_result = u'ผ่าน'
            else:
                review_result = u'ไม่ผ่าน'                
            submission_status = submission_status + (
u"""
สถานะการตรวจสอบ: ตรวจสอบแล้ว เมื่อ %(doc_review_at)s
ผลการตรวจสอบ: %(doc_review_status)s
""" % { 'doc_review_at': applicant.submission_info.doc_reviewed_at.strftime("%H:%M, %d %b"),
        'doc_review_status': review_result })
            
        else:
            # has not been reviewed
            if applicant.submission_info.doc_received_at != None:
                doc_received_status = u"ได้รับเมื่อ " + applicant.submission_info.doc_received_at.strftime("%H:%M, %d %b")
            else:
                doc_received_status = u"ยังไม่ได้รับ"
            submission_status = submission_status + (
                u"""
สถานะการตรวจสอบ: ยังไม่ได้ตรวจสอบ
สถานะใบสมัคร: %(doc_received_status)s""" % { 'doc_received_status': doc_received_status })
            
    else:
        # not submitted
        ticket_number = u'ไม่มีหมายเลขผู้สมัคร'
        submission_status = u"สถานะใบสมัคร: ยังไม่ได้ยืนยัน"

    if not applicant.has_major_preference():
        pref_status = u"ยังไม่ได้เลือกอันดับของสาขา"
    else:
        pref_status = (u"อันดับของสาขาที่เลือกคือ:\n" + 
                       u'\n'.join([unicode(m) for m in  applicant.preference.get_major_list()]))
    status = (
u"""ชื่อ: %(full_name)s
หมายเลขผู้สมัคร: %(ticket_number)s
วิธีการส่งใบสมัคร: %(doc_submission_method)s

%(submission_status)s
%(pref_status)s
""" % { 
            'full_name': applicant.full_name(),
            'ticket_number': ticket_number,
            'doc_submission_method': applicant.get_doc_submission_method_display(),
            'submission_status': submission_status,
            'pref_status': pref_status
            }
)
    return status


def send_status_by_email(applicant, force=False):
    subject = 'สถานะการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'
    message = (
u"""เรียนคุณ %(first_name)s %(last_name)s

ด้านล่างเป็นข้อมูลการสมัครเข้าศึกษาต่อแบบรับตรงประจำปีการศึกษา 2553
คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน
พร้อมด้วยลำดับการเลือกสาขาของคุณ
โปรดตรวจสอบ และถ้าพบข้อผิดพลาดให้รีบแจ้งกับทางผู้ดูแล
ทางอีเมล์ %(admin_email)s โดยด่วน

%(status)s
ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'first_name': applicant.first_name,
    'last_name': applicant.last_name,
    'status': summarize_applicant_status(applicant), 
    'admin_email': admin_email()
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_status_by_email_many_submitted_apps(applicants, force=False):
    subject = 'สถานะการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    statuses = u''
    counter = 1
    for a in applicants:
        statuses = statuses + (u"รายการที่ " + unicode(counter) + u"\n\n" + 
                               summarize_applicant_status(a) + u"\n")
        counter += 1

    message = (
u"""เรียนผู้ใช้อีเมล์ %(email)s

ระบบพบว่ามีข้อมูลของผู้ใช้หลายคนที่ใช้อีเมล์ %(email)s และมีการยื่นใบสมัครหลายครั้ง

ทั้งนี้สาเหตุอาจมาจากการส่งหลักฐานซ้ำซ้อน หรือการที่ทางเจ้าหน้าที่ป้อนข้อมูลซ้ำเข้าในระบบ
ข้อมูลซ้ำซ้อนนี้ไม่เป็นปัญหาต่อผู้สมัครแต่อย่างใด เพราะในการคัดเลือก 
คณะจะใช้ข้อมูลของผู้สมัครที่ผ่านการตรวจสอบเท่านั้น และจะตัดข้อมูลที่ไม่ผ่านทิ้งไป
อย่างไรก็ตาม ถ้ามีข้อมูลผ่านหลายชุดและผู้สมัครต้องการเลือกรายการที่ต้องการ
ให้รีบติดต่อกับทางผู้ดูแลทางอีเมล์ %(admin_email)s โดยด่วน

ด้านล่างเป็นข้อมูลการสมัครเข้าศึกษาต่อแบบรับตรงประจำปีการศึกษา 2553
คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน
พร้อมด้วยลำดับการเลือกสาขาของคุณ
โปรดตรวจสอบ และถ้าพบข้อผิดพลาดให้รีบแจ้งกับทางผู้ดูแล
ทางอีเมล์ %(admin_email)s โดยด่วน

%(statuses)s
ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'email': applicants[0].get_email(),
    'statuses': statuses,
    'admin_email': admin_email()
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicants[0].get_email(), subject, message, force)



def send_admission_status_problem_by_mail(email, force=False):
    subject = 'ผลการสมัครเข้าศึกษาต่อแบบรับตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    message = (
u"""เรียนผู้ใช้อีเมล์ %(email)s

ในการเรียกค้น เราพบว่ามีข้อมูลผู้ใช้หลายคนที่มีหมายเลขประจำตัวประชาชนไม่ตรงกันที่ใช้อีเมล์นี้
ทำให้เราไม่สามารถตรวจสอบผลการรับสมัครให้แบบอัตโนมัติได้

รบกวนผู้สมัครส่งเมล์สอบถามผลการรับสมัครโดยตรงที่ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'email': email,
    'admin_email': admin_email()
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicants[0].get_email(), subject, message, force)


def send_admission_status_by_mail(applicant, force=False):
    subject = u'ผลการสมัครเข้าศึกษาต่อแบบรับตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    if applicant.has_admission_result():
        if applicant.admission_result.is_waitlist:
            result = u"""คุณมีชื่ออยู่ในรายชื่อสำรอง ดูข้อมูลเพิ่มเติมได้จาก<a href="http://admission.eng.ku.ac.th/adm/%s">หน้าประกาศผล</a>
สำหรับผู้ที่มีรายชื่ออยู่ในรายชื่อสำรอง คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์จะประกาศรายชื่อผู้มีสิทธิ์เข้าสอบสัมภาษณ์ในวันศุกร์ที่ 5 กุมภาพันธ์ 2553 ทางเว็บไซด์ <a href="http://admission.eng.ku.ac.th">โครงการรับตรง (http://admission.eng.ku.ac.th)</a>""" % (reverse("result-set-index", args=["waitlist"]),)
        else:
            result = u"""คุณผ่านการคัดเลือกให้เข้ารับการสัมภาษณ์เข้าศึกษาต่อแบบรับตรง (ดูข้อมูลเพิ่มเติมได้ที่<a href="http://admission.eng.ku.ac.th/adm/%(url)s">หน้าประกาศผลการรับสมัคร</a>)

สาขาที่ได้รับการคัดเลือก*: %(major)s
ข้อมูลการสัมภาษณ์: %(add_info)s

หมายเหตุ: สาขาที่ได้รับคัดเลือกอาจมีการเปลี่ยนแปลงได้ แต่จะเป็นสาขาที่อยู่ในอันดับที่ดีขึ้นเท่านั้น""" % {
                'url': reverse('result-set-index', args=['admitted']),
                'major':
                    (applicant.admission_result.admitted_major.number + ' ' + 
                     applicant.admission_result.admitted_major.name),
                'add_info': applicant.admission_result.additional_info }
    else:
        result = u"""คุณไม่ผ่านการคัดเลือกให้เข้ารับการสัมภาษณ์รอบที่ 1 อย่างไรก็ตาม ในวันที่ 5 ก.พ. 2553 จะมีการประกาศรายชื่อผู้มีสิทธิ์เพิ่มเติม กรุณาติดตามได้จากเว็บรับตรง 

นอกจากนี้ยังมีช่องทางอื่นในการเข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตบางเขน กรุณาดูข้อมูลได้ที่เว็บ <a href="http://admission.eng.ku.ac.th/information/2553">http://admission.eng.ku.ac.th</a>"""

    message = (
u"""เรียนคุณ %(first_name)s %(last_name)s

ด้านล่างเป็นผลการสมัครเข้าศึกษาต่อแบบรับตรงประจำปีการศึกษา 2553
คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน

%(result)s

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'first_name': applicant.first_name,
    'last_name': applicant.last_name,
    'result': result,
    'admin_email': admin_email()
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_final_admission_status_by_mail(applicant, force=False):
    subject = u'ผลการสมัครเข้าศึกษาต่อแบบรับตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    if applicant.has_admission_result():
        admission_result = applicant.admission_result
    else:
        from result.models import AdmissionResult

        admission_result = AdmissionResult.new_for_applicant(applicant)

    from django.template.loader import get_template
    from django.template import Context

    result = (get_template('emails/final_admission_status.txt')
              .render(Context({'applicant': applicant,
                               'admission_result': admission_result})))

    message = (
u"""เรียนคุณ %(first_name)s %(last_name)s

ด้านล่างเป็นผลการสมัครเข้าศึกษาต่อแบบรับตรงประจำปีการศึกษา 2553
คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน

%(result)s

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'first_name': applicant.first_name,
    'last_name': applicant.last_name,
    'result': result,
    'admin_email': admin_email()
    }
).replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)

