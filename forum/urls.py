from django.conf.urls import url

from forum import views

urlpatterns = [
    url(r'^$',views.articles,name="create_forums"),
    url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
    url(r'^write$', views.CreateArticle, name='write'),
    url(r'^comment/', views.comment, name='comment'),
]  
