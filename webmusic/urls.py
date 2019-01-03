__author__ = "JentZhang"

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^collect', views.collect),
    url(r'^search', views.search),
    url(r'^get_search_result', views.get_search_result),
]
