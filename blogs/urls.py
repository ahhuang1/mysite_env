"""mysite_env URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from blogs import views

urlpatterns = [
    url(r'^$',views.blogs_index,name='blog_index'),
    url(r'^add/$',views.blogs_add,name='blogs_add'),
    url(r'^manage/$',views.blogs_list,name='blogs_list'),
    url(r'^manage/delete/$',views.blogs_delete,name='blogs_delete'),
    url(r'^edit/(\d+)/$',views.blogs_edit,name='blog_edit'),
    url(r'^blogs_detail/(\d+)/$',views.blogs_detail,name='blog_detail'),
    url(r'^blogs_detail/(\d+)/comment/$',views.blogs_comment,name='blog_dcomment'),
]
