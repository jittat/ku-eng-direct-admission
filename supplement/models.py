from django.db import models

from application.fields import IntegerListField
from application.models import Applicant
from upload.models import uploaded_storage, get_doc_path

class SupplementType(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']

def get_supplement_path(instance, filename):
    return get_doc_path(instance.applicant, 'supplements')

class Supplement(models.Model):
    applicant = models.ForeignKey(Applicant, related_name='supplements')
    supplement_type = models.ForeignKey(SupplementType)
    image = models.ImageField(
        upload_to=get_supplement_path,
        storage=uploaded_storage,
        blank=True)

    def __unicode__(self):
        return (u'Supplement for %d (type: %d)' % 
                (self.applicant_id,
                 self.supplement_type_id))


