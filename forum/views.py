from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render,redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

import markdown
from forum.forms import ArticleForm
from forum.models import Article, ArticleComment
from forum.decorators import ajax_required


def _articles(request, articles):
	paginator = Paginator(articles, 10)
	page = request.GET.get('page')
	try:
		articles = paginator.page(page)

	except PageNotAnInteger:
		articles = paginator.page(1)

	except EmptyPage:
		articles = paginator.page(paginator.num_pages)

	# popular_tags = Article.get_counted_tags()

	return render(request, 'community.html', {'articles':articles})

# class CreateArticle(LoginRequiredMixin, CreateView):
# 	template_name = 'writeforum.html'
# 	form_class = ArticleForm
# 	success_url = reverse_lazy('community')

# 	def form_valid(self,form):
# 		form.instance.create_user = self.request.user
# 		return super(CreateArticle,self).form_valid(form)
@login_required
def CreateArticle(request):
	path = request.path
	if request.method == 'POST':
		form = ArticleForm(data=request.POST, auto_id="%s")
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]

			status = 'P'
			create_user = request.user
			update_user = request.user
			article = Article(title=title,content=content,create_user=create_user,
								update_user=update_user,status=status)
			
			article.save()
			path = path[0:path.rfind('write')]
			print(path)
			return redirect(path)
	else:
		form = ArticleForm(auto_id="%s")

	return render(request,"writeforum.html",locals())


class EditArticle(LoginRequiredMixin, UpdateView):
	template_name = 'edit.html'
	model = Article
	form_class = ArticleForm
	success_url = reverse_lazy('articles')

@login_required
def articles(request):
	all_articles = Article.get_published()
	return _articles(request, all_articles)

@login_required
def article(request,slug):
	article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)
	return render(request, 'page.html', {'article':article})

# @login_required
# def tag(request,tag_name):
# 	articles = Article.objects.filter(tags__name=tag_name).filter(status='P')
# 	return _articles(request,articles)

@login_required
def drafts(request):
	drafts = Article.objects.filter(create_user=request.user,
									status = Article.DRAFT)
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


# @login_required
# @ajax_required
# def comment(request):
# 	try:
# 		if request.method == 'POST':
# 			article_id = request.POST.get('article')
# 			article = Article.objects.get(pk=article_id)
# 			comment = request.POST.get('comment')
# 			comment = comment.strip()
# 			if len(comment) > 0:
# 				article_comment = ArticleComment(user=request.user,
# 												aticles=article,
# 												comment=comment)
# 				article_comment.save()
# 			html = ''

# 			for comment in article.get_comments():
# 				html = '{0}{1}'.format(html.render_to_string('partial_article_comment.html',
# 										{'comment':comment}))
# 			return HttpResponse(html)

# 		else:
# 			return HttpResponseBadRequest()

# 	except Exception:
# 		return HttpResponseBadRequest()

@login_required
# @ajax_required
def comment(request):
	if request.method == 'POST':
		article_id = request.POST.get('article')
		article = Article.objects.get(pk=article_id)
		comment = request.POST.get('comment')
		comment = comment.strip()
		if len(comment) > 0:
			article_comment = ArticleComment(user=request.user,aticles=article,comment=comment)
			article_comment.save()

		return render(request,'page.html',{'article':article})
	else:
		return HttpResponseBadRequest()