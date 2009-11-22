from django.db import models

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

