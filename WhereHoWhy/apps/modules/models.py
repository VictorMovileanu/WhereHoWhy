import uuid
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Quote(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    text = models.TextField()
    source = models.CharField(max_length=256)

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
        FieldPanel('source'),
    ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('modules:quote', kwargs={'uuid': self.uuid})
