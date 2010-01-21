from django.conf.urls.defaults import *

urlpatterns = patterns(
    'confirmation.views',

    url(r'^/$', 'index', name='confirmation-index'),

    url(r'^submit/$', 'confirm', 
        {'preview': True}, name='confirmation-submit'),
    url(r'^confirm/$', 'confirm', name='confirmation-confirm'),

    url(r'^pref/$', 'pref', name='confirmation-pref'),
    url(r'^info/(\d+)/$', 'interview_info', name='confirmation-info'),
)
