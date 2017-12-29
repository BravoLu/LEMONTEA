from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Account(AbstractUser):
    class Meta:
        db_table = "Account"

    def __str__(self):
        return self.username

class Course(models.Model):
    college_name = models.CharField("大学", max_length=50, null=True)
    course_order = models.IntegerField("课程编号", null=True)
    course_identifier = models.CharField("课程号", max_length=50)
    title = models.CharField("课程名称", max_length=50)
    image = models.ImageField(upload_to="CoursePhoto/", null=True, default="CoursePhoto/default.png")
    description = models.TextField("课程介绍")
    teacher = models.CharField("授课老师", max_length=50)
    class Meta:
        db_table = "Course"

    def __str__(self):
        return self.title

class ChapterList(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter_order = models.IntegerField("章节编号")
    title = models.CharField("章节标题", max_length=50)
    description = models.TextField("章节介绍")
    class Meta:
        unique_together = ("id", "course_id")
        db_table = "ChapterList"

    def __str__(self):
        return self.title

class PPTList(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter_id = models.ForeignKey(ChapterList, on_delete=models.CASCADE)
    ppt_order = models.IntegerField("PPT编号")
    title = models.CharField("PPT标题", max_length=50)
    path = models.CharField("PPT路径", max_length=100)
    class Meta:
        unique_together = ("id", "course_id", "chapter_id")
        db_table = "PPTList"

    def __str__(self):
        return self.title

