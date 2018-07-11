"""pyblog URL Configuration

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
from django.conf.urls import re_path
from pyblog1 import BlogDetailView, BlogListView, LatestEntriesFeed
from django.contrib import admin
from pyblog1 import views
urlpatterns =[
re_path(r'^index', views.index, name='index'),
    re_path(r'^SignUp', views.SignUp, name='SignUp'),
    re_path(r'^Login', views.Login, name='Login'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-_\w]+)/$',
                    BlogDetailView.as_view(),
                    name='blog_detail',
                    ),
    re_path(r'^archive/$',
                    BlogListView.as_view(
                        template_name="simpleblog/post_archive.html",
                        page_template="simpleblog/post_archive_page.html"),
                        name="blog_archive"),
    re_path(r'^latest/feed/$', LatestEntriesFeed()),
    re_path(r'^$', BlogListView.as_view(), name='blog_index'),

]

