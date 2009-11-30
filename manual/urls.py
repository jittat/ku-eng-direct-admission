from django.conf.urls.defaults import *

urlpatterns = patterns(
    'manual.views',

    url(r'^$', 'index', name='manual-index'),
    url(r'^create/$', 'create', name='manual-create'),
    url(r'^personal/(\d+)/$', 'personal_form', name='manual-personal'),
    url(r'^address/(\d+)/$', 'address_form', name='manual-address'),
    url(r'^education/(\d+)/$', 'edu_form', name='manual-edu'),
    url(r'^majors/(\d+)/$', 'major_form', name='manual-majors'),
    url(r'^confirm/(\d+)/$', 'manual_confirm', name='manual-confirm'),

    url(r'^education/(\d+)/edit/$', 'edu_form', 
        {'edit': True, 'popup': True}, name='manual-edu-popup'),

    # ajax call
    url(r'^show/edu/(\d+)/$', 'show_edu', name='manual-show-edu'),
)
