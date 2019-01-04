__author__ = "JentZhang"

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^get_search_result', views.get_search_result),
    url(r'^get_home_data', views.get_home_data),
]
