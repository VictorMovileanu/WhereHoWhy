from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from frontpage.models import Tweet, Project, Post


class PostAdminForm(SummernoteModelAdmin):
    summernote_fields = '__all__'


admin.site.register(Tweet)
admin.site.register(Project)
admin.site.register(Post, PostAdminForm)
