import os.path
from random import randint

from django.db import models
from django.core.urlresolvers import reverse

from application.fields import IntegerListField
from application.models import Applicant
from upload.models import uploaded_storage, get_doc_path, get_doc_fullpath
from commons.utils import random_string

class SupplementType(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']

def get_supplement_path(instance, filename):
    fname, ext = os.path.splitext(filename)
    random_filename = 'supplement-%d%s' % (randint(1,1000000),ext)
    return get_doc_path(instance.applicant, random_filename)

def get_preview_path(supplement):
    return get_doc_fullpath(supplement.applicant, 
                            'supplement-preview-%d.png' % (supplement.id,))

class Supplement(models.Model):
    applicant = models.ForeignKey(Applicant, related_name='supplements')
    supplement_type = models.ForeignKey(SupplementType)
    image = models.ImageField(
        upload_to=get_supplement_path,
        storage=uploaded_storage,
        blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __unicode__(self):
        return (u'Supplement for %d (type: %d)' % 
                (self.applicant_id,
                 self.supplement_type_id))

    def random_string(self):
        return random_string(5)

    def render_view_link(self):
        full_name = self.image.path
        fname, ext = os.path.splitext(full_name)
        new_name = '%d%s' % (self.id, ext)
        return reverse('review-supplement-img-view',
                       args=[new_name])

    def preview_path(self):
        return get_preview_path(self)

    def create_preview(self):
        preview_filename = self.preview_path()
        filename = self.image.path

        import Image
        
        im = Image.open(filename)
        if im.size[0] > im.size[1]:
            size = 400,300
        else:
            size = 300,400
        im.thumbnail(size)

        im.save(preview_filename,'png')
