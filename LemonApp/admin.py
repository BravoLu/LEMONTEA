from django.contrib import admin
from LemonApp.models import Account, Course, ChapterList, PPTList
# Register your models here.
admin.site.register([Account, Course, ChapterList, PPTList])