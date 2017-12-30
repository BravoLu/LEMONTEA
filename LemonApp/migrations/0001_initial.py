# Generated by Django 2.0 on 2017-12-30 10:09

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_order', models.IntegerField(verbose_name='章节编号')),
                ('title', models.CharField(max_length=50, verbose_name='章节标题')),
                ('description', models.TextField(verbose_name='章节介绍')),
            ],
            options={
                'db_table': 'ChapterList',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='大学名字')),
                ('english_name', models.CharField(max_length=100, verbose_name='英文名字')),
                ('image', models.ImageField(default='CollegePhoto/default.png', null=True, upload_to='CollegePhoto/', verbose_name='大学图片')),
                ('description', models.TextField(verbose_name='大学介绍')),
            ],
            options={
                'db_table': 'College',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_order', models.IntegerField(null=True, verbose_name='课程编号')),
                ('course_identifier', models.CharField(max_length=50, verbose_name='课程号')),
                ('title', models.CharField(max_length=50, verbose_name='课程名称')),
                ('image', models.ImageField(default='CoursePhoto/default.png', null=True, upload_to='CoursePhoto/', verbose_name='课程图片')),
                ('description', models.TextField(verbose_name='课程介绍')),
                ('teacher', models.CharField(max_length=50, verbose_name='授课老师')),
                ('college_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LemonApp.College')),
            ],
            options={
                'db_table': 'Course',
            },
        ),
        migrations.CreateModel(
            name='PPTImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_order', models.IntegerField(verbose_name='PPT图片编号')),
                ('image', models.ImageField(upload_to='PPTPhoto/', verbose_name='PPT图片')),
            ],
            options={
                'db_table': 'PPTImage',
            },
        ),
        migrations.CreateModel(
            name='PPTList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ppt_order', models.IntegerField(verbose_name='PPT编号')),
                ('title', models.CharField(max_length=50, verbose_name='PPT标题')),
                ('file', models.FileField(upload_to='PPT/', verbose_name='PPT文件')),
                ('chapter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LemonApp.ChapterList')),
            ],
            options={
                'db_table': 'PPTList',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('face', models.ImageField(default='UserPhoto/default.png', null=True, upload_to='UserPhoto/', verbose_name='头像')),
                ('permission', models.IntegerField(default=0, verbose_name='权限类型')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Account',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='pptimage',
            name='ppt_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LemonApp.PPTList'),
        ),
        migrations.AddField(
            model_name='course',
            name='creator_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chapterlist',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LemonApp.Course'),
        ),
        migrations.AlterUniqueTogether(
            name='pptlist',
            unique_together={('id', 'chapter_id')},
        ),
        migrations.AlterUniqueTogether(
            name='pptimage',
            unique_together={('id', 'ppt_id')},
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('id', 'college_id', 'creator_id')},
        ),
        migrations.AlterUniqueTogether(
            name='chapterlist',
            unique_together={('id', 'course_id')},
        ),
    ]
