from django.core.mail import send_mail
from django.conf import settings

def send_applicant_email(applicant, password):
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
    sender = 'admin@admission.eng.ku.ac.th'

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
                  [ applicant.email ],
                  fail_silently=True)
    else:
        print 'Does not send email'
        print 'Message:'
        print message

