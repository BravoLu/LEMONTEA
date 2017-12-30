from django.contrib import admin
from LemonApp.models import Account, College, Course, ChapterList, PPTList
# Register your models here.
admin.site.register([Account, College, Course, ChapterList, PPTList])