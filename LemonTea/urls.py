"""LemonTea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from LemonApp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^school/$', views.school, name='school'),
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^$', views.home, name="home"),
    url(r'login$', views.login, name="login"),
    url(r'signup$', views.signup, name="signup"),
    url(r'^logout$', views.logout_view, name="logout"),
    url(r'^share', views.share, name="share"),
    url(r'^study', views.study, name="study"),
    url(r'course/[0-9]+/$', views.course, name="course"),
    url(r'^shop', views.shop, name="shop"),
    url(r'^identity', views.identity, name="identity"),
    url(r'^community', views.community ,name='community'),
    url(r'^page',views.page, name="page"),
    url(r'create_course$',views.create_course, name="create_course"),
    url(r'^add_chapter$',views.add_chapter, name="add_chapter"),
    url(r'^add_ppt$',views.add_ppt, name="add_ppt"),
    url(r'^testpage$',views.testpage, name="testpage"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
