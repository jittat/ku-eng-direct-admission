from django.conf.urls.defaults import *

urlpatterns = patterns(
    'confirmation.views',

    url(r'^pref/$', 'pref', name='confirmation-pref'),
    url(r'^info/(\d+)/$', 'interview_info', name='confirmation-info'),
)
