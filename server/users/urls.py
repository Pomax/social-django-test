from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout', views.forceLogout, name='logout'),
    url(r'^oauth2callback', views.callback, name='oauthcallback'),
]
