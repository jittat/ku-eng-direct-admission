from django.template import Library

from commons.utils import admin_email

register = Library()


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
