__author__ = "JentZhang"

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^get_search_result', views.get_search_result),
    url(r'^get_home_data', views.get_home_data),
    url(r'^get_album_info/(?P<albumId>[0-9]+)', views.get_album_info),
    url(r'^GetCode', views.get_code),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^collect_action', views.collect_action),
]
