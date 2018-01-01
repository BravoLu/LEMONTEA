from django.conf.urls import url

from forum import views

urlpatterns = [
	url(r'^M$', views.math,name="math"),
	url(r'^E$',views.foreign,name="foreign"),
    url(r'^C$',views.articles,name="create_forums"),
    url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
    url(r'^[A-Z]/write/$', views.CreateArticle, name='write'),
    url(r'^comment', views.comment, name='comment'),
]  
