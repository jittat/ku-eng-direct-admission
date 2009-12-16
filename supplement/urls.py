from django.conf.urls.defaults import *

urlpatterns = patterns(
    'supplement.views',
    url(r'^$', 'index', name='supplement-index'),
    url(r'^upload/$', 'upload', name='supplement-upload'),
    url(r'^view/(\d+)\.png$', 'supp_get_img', name='supplement-preview'),
    url(r'^delete/(\d+)/$', 'delete_supplement', name='supplement-delete'),
)

