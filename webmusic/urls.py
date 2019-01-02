__author__ = "JentZhang"

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'charts', views.charts),
    url(r'collect', views.collect),
    url(r'artist', views.artist),
    url(r'search', views.search),
]
