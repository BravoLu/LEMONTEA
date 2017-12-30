from __future__ import unicode_literals

from django.db import models
from LemonApp.models import Account
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

import markdown
from taggit.managers import TaggableManager

# Create your models here.

class Forum(models.Model):
	DRAFT = 'D'
	PUBLISHED = 'P'
	STATUS = (
		(DRAFT,'Draft'),
		(PUBLISHED,'Published'),
	)

	title = models.CharField(max_length=255,null=False,unique=True)
	slug = AutoSlugField(populate_from='title')
	# tags = TaggableManager()
	content = models.TextField(max_length=4000)
	status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
	create_user = models.ForeignKey(Account,on_delete=models.CASCADE)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)
	update_user = models.ForeignKey(Account,null=True,blank=True,
									related_name="+",on_delete=models.CASCADE)


	class Meta:
		verbose_name = _("Forum")
		verbose_name_plural = _("Forums")
		ordering = ("-create_date",)		

	def __str__(self):
		return self.title

	def get_content_as_markdown(self):
		return markdown.markdown(self.content,safe_mode='escape')

	#使得类不需要实例化就能调用
	@staticmethod
	def get_published():
		forums1 = Forum.objects.filter(status=Forum.PUBLISHED)
		return forums1

	# @staticmethod
	# def get_counted_tags():
	# 	tag_dict = {}
	# 	query = Forum.objects.filter(status='P').annotate(tagged=Count(
	# 		'tags')).filter(tags__gt=0)
	# 	for obj in query:
	# 		for tag in obj.tags.names():
	# 			if tag not in tag_dict:
	# 				tag_dict[tag] = 1
	# 			else:
	# 				tag_dict[tag] += 1

	# 	return tag.dict.items()

	def get_summary(self):
		if len(self.content) > 255:
			return '{0}...'.format(self.content[:255])
		else:
			return self.content

	def get_summary_as_markdown(self):
		return markdown.markdown(self.get_summary(),safe_mode='escape')

	def get_comments(self):
		return ForumComment.objects.filter(forums=self)


class ForumComment(models.Model):
	forums = models.ForeignKey(Forum,on_delete=models.CASCADE)
	comment = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(Account,on_delete=models.CASCADE)

	class Meta:
		verbose_name = _("Forum Comment")
		verbose_name_plural = _("Forum Comments")
		ordering = ("date",)

	def __str__(self):
		return '{0} - {1}'.format(self.user.username, self.forums.title)

	def get_comment_as_markdown(self):
		return markdown.markdown(self.comment, safe_mode='escape')