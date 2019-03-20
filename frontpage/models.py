from django.db import models
from django.utils import timezone


class Tweet(models.Model):
    created = models.DateTimeField()
    quote = models.TextField()
    source = models.CharField(max_length=1024)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Tweet, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
