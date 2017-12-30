from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy

import markdown
from forum.forms import ForumForm
from forum.models import Forum, ForumComment
from forum.decorators import ajax_required


def _forums(request, articles):
	paginator = Paginator(articles, 10)
	page = request.GET.get('page')
	try:
		articles = paginator.page(page)

	except PageNotAnInteger:
		articles = paginator.page(1)

	except EmptyPage:
		articles = paginator.page(paginator.num_pages)

	# popular_tags = Forum.get_counted_tags()

	return render(request, 'writeforum.html', {'articles':articles})

class CreateForum(LoginRequiredMixin, CreateView):
	template_name = 'writeforum.html'
	form_class = ForumForm
	success_url = reverse_lazy('create_forums')

	def form_valid(self,form):
		form.instance.create_user = self.request.user
		return super(CreateForum,self).form_valid(form)

class EditForum(LoginRequiredMixin, UpdateView):
	template_name = 'edit.html'
	model = Forum
	form_class = ForumForm
	success_url = reverse_lazy('articles')

@login_required
def articles(request):
	all_articles = Forum.get_published()
	return _articles(request, all_articles)

@login_required
def article(request,slug):
	article = get_object_or_404(Forum, slug=slug, status=Forum.PUBLISHED)
	return render(request, 'page.html', {'article':article})

# @login_required
# def tag(request,tag_name):
# 	articles = Forum.objects.filter(tags__name=tag_name).filter(status='P')
# 	return _articles(request,articles)

@login_required
def drafts(request):
	drafts = Forum.objects.filter(create_user=request.user,
									status = Forum.DRAFT)
	return render(request,'drafts.html',{'drafts':drafts})


@login_required
@ajax_required
def preview(request):
	try:
		if request.method == 'POST':
			content = request.POST.get('content')
			html = 'Nothing to display :('
			if len(content.strip()) > 0:
				html = markdown.markdown(content,safe_mode='escape')
			return HttpResponse(html)

		else:
			return HttpResponse()

	except Exception:
		return HttpResponseBadRequest()


@login_required
@ajax_required
def comment(request):
	try:
		if request.method == 'POST':
			article_id = request.POST.get('article')
			article = Forum.objects.get(pk=article_id)
			comment = request.POST.get('comment')
			comment = comment.strip()
			if len(comment) > 0:
				article_comment = ForumComment(user=request.user,
												forums=article,
												comment=comment)
				article_comment.save()
			html = ''
			for comment in article.get_comments():
				html = '{0}{1}'.format(html.render_to_string('partial_article_comment.html',
										{'comment':comment}))
			return HttpResponse(html)

		else:
			return HttpResponseBadRequest()

	except Exception:
		return HttpResponseBadRequest()