from django.conf.urls.defaults import *

urlpatterns = patterns(
    'result.views',

    url(r'^$', 'list', name='result-index'),
    url(r'^page/(\d+)/$', 'list', name='result-page'),
)
