# Talk urls
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'talk.views',
    url(r'^$', 'home'),
    url(r'^browsing/$', 'browsing'),
    url(r'^text_process/$', 'text_process'),
    url(r'^image_process/$', 'image_process'),
    url(r'^text_image_process/$', 'text_image_process'),
    url(r'^video_process/$', 'video_process'),
)
