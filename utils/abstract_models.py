from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
