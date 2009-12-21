from django.db import models
from django.contrib.auth.models import User

class Announcement(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField()
    is_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        if len(self.body)>100:
            body = self.body[:100] + "..."
        else:
            body = self.body

        return "(%s) %s" % (str(self.created_at),body)

    @staticmethod
    def get_all_enabled_annoucements():
        return Announcement.objects.filter(is_enabled=True).all()

class Log(models.Model):
    user = models.CharField(max_length=20)
    message = models.CharField(max_length=100)
    applicant_id = models.IntegerField(blank=True, null=True)
    applicantion_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def create(message, user='', applicant_id=None, applicantion_id=None):
        if isinstance(user,User):
            user = user.username
        log = Log(user=user, message=message,
                  applicant_id=applicant_id, applicantion_id=applicantion_id)
        log.save()
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.message)

