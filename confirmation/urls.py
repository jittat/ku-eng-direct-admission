from django.conf.urls.defaults import *

urlpatterns = patterns(
    'confirmation.views',

    url(r'^pref/$', 'pref', name='confirmation-pref'),
)
