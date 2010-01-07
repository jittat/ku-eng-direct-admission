from django.conf.urls.defaults import *

urlpatterns = patterns(
    'result.views',

    url(r'^$', 'index', name='result-index'),
    url(r'^(\w+)/$', 'list', name='result-set-index'),
    url(r'^(\w+)/page/(\d+)/$', 'list', name='result-set-page'),
)
