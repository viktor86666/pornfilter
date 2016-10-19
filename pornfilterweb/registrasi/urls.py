# Talk urls
from django.conf.urls import patterns, url
from registrasi import views
from django.contrib import admin
from django.conf import settings
urlpatterns = patterns(
    'registrasi.views',
    url(r'^registrasi/$', 'registrasi'),
    url(r'^registrasi/save_registration/$', 'save_registration'),
    url(r'^user/$', views.user_list, name='user_list'),
    url(r'^user/search/$', views.user_search, name='user_search'),
    url(r'^user/add/$', views.user_edit, name='user_add'),
    url(r'^user/mod/(?P<user_id>\d+)/$', views.user_edit, name='user_mod'),
    url(r'^user/del/(?P<user_id>\d+)/$', views.user_del, name='user_del'),

)
