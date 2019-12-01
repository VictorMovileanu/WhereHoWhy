from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField

from utils.abstract_models import TimeStampedModel

USER_MODEL = get_user_model()


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


class Project(TimeStampedModel):
    name = models.CharField(
        verbose_name=_("Project name"),
        max_length=100
    )
    master = models.ForeignKey(
        USER_MODEL,
        verbose_name=_("Project Leader"),
        on_delete=models.SET_NULL,
        null=True
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("Groups"),
        blank=True,  # this means groups are optional
        help_text=_("Groups that have additional permissions on instances of this model")
    )
    is_public = models.BooleanField(default=True)
    logo = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg", ".png"], blank=False)
    url = models.URLField(
        verbose_name=_("Project detail URL")
    )


class Post(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        verbose_name=_("Project"),
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        null=True
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("Groups"),
        blank=True,  # this means groups are optional
        help_text=_("Groups that have additional permissions on instances of this model")
    )
    is_public = models.BooleanField(default=True)
    text = models.TextField()
