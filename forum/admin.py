from django.contrib import admin
from forum.models import Article,ArticleComment
# Register your models here.
admin.site.register([Article,ArticleComment])
