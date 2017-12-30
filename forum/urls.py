from django.conf.urls import url

from forum import views

urlpatterns = [
    url(r'^writeforum',views.CreateForum.as_view(),name="create_forums"),
]
