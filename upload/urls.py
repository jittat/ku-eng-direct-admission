from django.conf.urls.defaults import *

urlpatterns = patterns(
    'upload.views',
    url(r'^$', 'index', name='upload-index'),
    url(r'^upload/(?P<field_name>\w*)/$', 'upload', name='upload-form'),
    url(r'^progress/$', 'upload_progress', name='upload-progress'),    
)
