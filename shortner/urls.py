from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^surl/$', views.showURLPage, name='showURLPage'),
    url(r'^shortenURL/$', views.shortenURL, name='shortenURL'),
    url(r'^url/(?P<shorturl>[a-z A-Z 0-9]+)/$', views.redirectToLongURL, name='redirectToLongURL'),
    url(r'^search/$', views.searchURL, name='searchURL'),
    url(r'^hits/$', views.getNoOfHits, name='getNoOfHits'),
]
