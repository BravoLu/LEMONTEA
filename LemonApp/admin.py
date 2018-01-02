from django.contrib import admin
from LemonApp.models import Account, College, TeacherInformation, StudentInformation, Course, ChapterList, PPTList, CourseComment, PPTComment
# Register your models here.
admin.site.register([Account, College, Course, TeacherInformation, StudentInformation, ChapterList, PPTList, CourseComment, PPTComment])