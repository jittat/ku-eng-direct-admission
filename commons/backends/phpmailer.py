import httplib
import urllib

from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.http import QueryDict

class EmailBackend(BaseEmailBackend):
    """
    An email backend for sending email through services provided by
    kidsdev.  Thanks!
    """

    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, **kwargs):
        super(EmailBackend, self).__init__(fail_silently=fail_silently)
        self.host = host or settings.EMAIL_HOST
        self.port = port or settings.EMAIL_PORT
        self.username = username or settings.EMAIL_HOST_USER
        self.password = password or settings.EMAIL_HOST_PASSWORD
        if use_tls is None:
            self.use_tls = settings.EMAIL_USE_TLS
        else:
            self.use_tls = use_tls
        try:
            self.key = settings.PHPMAILER_KEY
        except:
            self.key = ''


    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number
        of email messages sent.
        """
        if not email_messages:
            return
        try:
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
        finally:
            pass
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        try:
            params = QueryDict('').copy()
            params.update({
                    'key': self.key,
                    'to': email_message.recipients()[0],
                    'body': email_message.body,
                    'subject': email_message.subject,
                    })
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            conn = httplib.HTTPConnection("%s:%d" %
                                          (self.host, self.port))
            conn.request("POST", 
                         "/webservice/phpmailer.php", 
                         params.urlencode(), 
                         headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return response.status == 202
        except:
            if not self.fail_silently:
                raise
            return False

