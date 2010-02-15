from django.conf.urls.defaults import *
from models import confirmation_resource

urlpatterns = patterns(
    'confirmation.views',

    url(r'^$', 'index', name='confirmation-index'),
    url(r'^stat/$', 'confirmation_stat', name='confirmation-stat'),
    url(r'^stat/download/$', 'confirmation_stat_download', name='confirmation-stat-download'),

    url(r'^submit/$', 'confirm', 
        {'preview': True}, name='confirmation-submit'),
    url(r'^confirm/$', 'confirm', name='confirmation-confirm'),

    url(r'^confirm-second-round/$', 'show_confirmation_second_round', name='confirmation-second'),
    url(r'^confirm-second-round-admin/(\d+)/$', 'admin_show_confirmation_second_round', name='confirmation-second-admin'),

    url(r'^pref/$', 'pref', name='confirmation-pref'),
    url(r'^info/(\d+)/$', 'interview_info', name='confirmation-info'),

    url(r'^list/(.*?)/?$', confirmation_resource),
)
