# -*- coding: utf-8 -*-
from datetime import timedelta

from django.template import Library

from commons.utils import admin_email
from commons.utils import time_to_submission_deadline, time_to_supplement_submission_deadline, time_to_round2_confirmation_deadline

register = Library()

def adm_submission_deadline_warning():
    time_left = time_to_submission_deadline()
    if (time_left > timedelta(0)) and (time_left < timedelta(hours=3)):
        return ('<div class="deadline-bar"><span class="deadline">เหลือเวลาอีก %d ชั่วโมง %d นาที ก่อนหมดเวลารับสมัคร</span></div>' %
                (time_left.seconds/3600, time_left.seconds%3600/60))
    supplement_time_left = time_to_supplement_submission_deadline()
    if (supplement_time_left > timedelta(0)) and (supplement_time_left < timedelta(hours=3)):
        return ('<div class="deadline-bar"><span class="deadline">เหลือเวลาอีก %d ชั่วโมง %d นาที ก่อนหมดเวลายื่นหลักฐานเพิ่มเติม</span></div>' %
                (supplement_time_left.seconds/3600, 
                 supplement_time_left.seconds%3600/60))
    round2_time_left = time_to_round2_confirmation_deadline()
    if (round2_time_left > timedelta(0)) and (round2_time_left < timedelta(hours=3)):
        return ('<div class="deadline-bar"><span class="deadline">เหลือเวลาอีก %d ชั่วโมง %d นาที ก่อนหมดเวลายืนยันการเข้าพิจารณาคัดเลือกโครงการรับตรง (รอบที่ 2) ลำดับสำรอง</span></div>' %
                (round2_time_left.seconds/3600, 
                 round2_time_left.seconds%3600/60))

    return ''


adm_submission_deadline_warning = register.simple_tag(adm_submission_deadline_warning)

def adm_admin_email():
    """
    Returns the email of the first admin from settings.py
    """
    return admin_email()
adm_admin_email = register.simple_tag(adm_admin_email)


def adm_admin_email_link():
    """
    Returns the link to send email to admin.
    """
    email = admin_email()
    return '<a href="mailto:%s">%s</a>' % (email, email)
adm_admin_email_link = register.simple_tag(adm_admin_email_link)

@register.filter(name="thai_date")
def thai_date(value):
    months = (u'ม.ค. ก.พ. มี.ค. เม.ย. พ.ค. มิ.ย. ก.ค. ส.ค. ก.ย. ต.ค. พ.ย. ธ.ค.'
              .split())
    return ("%d %s %d" %
            (value.day, months[value.month-1], value.year + 543))


