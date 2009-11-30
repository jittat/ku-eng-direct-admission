from django.db import models
from application.models import Applicant
from application.fields import IntegerListField

class AdminEditLog(models.Model):
    applicant = models.ForeignKey(Applicant)
    message = models.TextField()

    def __unicode__(self):
        return self.applicant.full_name()

