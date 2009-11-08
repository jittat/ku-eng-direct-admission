from django.core.mail import send_mail
from django.conf import settings
from commons.utils import admin_email

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
    subject = 'Your account for applying at KU Engineering'
    message = (
u"""Dear %(firstname)s %(lastname)s

Thank you for applying at the Faculty of Engineering, Kasetsart University.

Your password is: %(password)s

Use your e-mail address (%(email)s) to log in.

Thank you.
-jittat"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.email, 
    'password': password }
)
    adm_send_mail(applicant.email, subject, message, force)
