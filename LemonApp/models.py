from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Account(AbstractUser):
    face = models.ImageField("头像", upload_to="UserPhoto/", null=True, default="UserPhoto/default.png")
    permission = models.IntegerField("权限类型", default=0) #数值越大权限越高
    class Meta:
        db_table = "Account"

    def __str__(self):
        return self.username

class College(models.Model):
    name = models.CharField("大学名字", max_length=100)
    english_name = models.CharField("英文名字", max_length=100)
    image = models.ImageField("大学图片", upload_to="CollegePhoto/", null=True, default="CollegePhoto/default.png")
    description = models.TextField("大学介绍")
    class Meta:
        db_table = "College"

    def __str__(self):
        return self.name

class Course(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    course_order = models.IntegerField("课程编号", null=True)
    course_identifier = models.CharField("课程号", max_length=50)
    title = models.CharField("课程名称", max_length=50)
    image = models.ImageField("课程图片", upload_to="CoursePhoto/", null=True, default="CoursePhoto/default.png")
    description = models.TextField("课程介绍")
    teacher = models.CharField("授课老师", max_length=50)
    class Meta:
        unique_together = ("id", "college_id", "creator_id")
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
    chapter_id = models.ForeignKey(ChapterList, on_delete=models.CASCADE)
    ppt_order = models.IntegerField("PPT编号")
    title = models.CharField("PPT标题", max_length=50)
    file = models.FileField("PPT文件", upload_to="PPT/")
    class Meta:
        unique_together = ("id",  "chapter_id")
        db_table = "PPTList"

    def __str__(self):
        return self.title

class PPTImage(models.Model):
    ppt_id = models.ForeignKey(PPTList, on_delete=models.CASCADE)
    image_order = models.IntegerField("PPT图片编号")
    image = models.ImageField("PPT图片", upload_to="PPTPhoto/")
    class Meta:
        unique_together = ("id",  "ppt_id")
        db_table = "PPTImage"

    def __str__(self):
        return self.image_order
