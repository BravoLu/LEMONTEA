from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Account(AbstractUser):
    face = models.ImageField("头像", upload_to="UserPhoto/", null=True, default="UserPhoto/default.png")
    permission = models.IntegerField("权限类型", default=0) #数值越大权限越高,1为普通用户,2为学生,3为老师,10为管理员
    college_id = models.IntegerField("所属大学", default=-1)
    card_number = models.CharField("学号或教工号", max_length=50, default="-1")
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

class TeacherInformation(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    is_bind = models.BooleanField("是否被绑定", default=False)
    TeacherID = models.CharField("教工号", max_length=50)

    class Meta:
        unique_together = ("college_id", "TeacherID")
        db_table = "TeacherInformation"

    def __str__(self):
        return self.TeacherID

class StudentInformation(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    is_bind = models.BooleanField("是否被绑定", default=False)
    StudentID = models.CharField("学号", max_length=50)

    class Meta:
        unique_together = ("college_id", "StudentID")
        db_table = "StudentInformation"

    def __str__(self):
        return self.StudentID

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

class CourseComment(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment_order = models.IntegerField("评论顺序")
    content = models.TextField("评论内容")
    class Meta:
        db_table = "CourseComment"

    def __str__(self):
        return "comment"

class PPTComment(models.Model):
    ppt_image_id = models.ForeignKey(PPTImage, on_delete=models.CASCADE)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment_order = models.IntegerField("评论顺序")
    content = models.TextField("评论内容")
    class Meta:
        db_table = "PPTComment"

    def __str__(self):
        return "comment"