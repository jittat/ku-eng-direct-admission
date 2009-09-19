from django.conf.urls.defaults import *

urlpatterns = patterns(
    'upload.views',
    url(r'^$', 'index', name='upload-index'),
    url(r'^upload/$', 'upload', name='upload-form'),
)
