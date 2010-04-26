from django.db import models

class Feature(models.Model):
    """
    >>> feature = Feature(name='feature1', disabled=False)
    >>> feature.save()
    >>> Feature.check_enabled('feature1')
    True
    """
    name = models.CharField(max_length=30,
                            unique=True)
    disabled = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def is_enabled(self):
        return not self.disabled

    def is_disabled(self):
        return self.disabled

    @staticmethod
    def check_enabled(name):
        try:
            feature = Feature.objects.get(name=name)
            return feature.is_enabled()
        except Feature.DoesNotExist:
            return False
