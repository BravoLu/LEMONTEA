from django.contrib import admin
from forum.models import Forum,ForumComment
# Register your models here.
admin.site.register([Forum,ForumComment])
