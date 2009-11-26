from django.conf.urls.defaults import *

urlpatterns = patterns(
    'manual.views',

    url(r'^$', 'index', name='manual-index'),
    url(r'^create/$', 'create', name='manual-create'),
    url(r'^personal/(\d+)/', 'personal_form', name='manual-personal'),
    url(r'^address/(\d+)/', 'address_form', name='manual-address'),
    url(r'^education/(\d+)/', 'edu_form', name='manual-edu'),
    url(r'^majors/(\d+)/', 'major_form', name='manual-majors'),
    url(r'^confirm/(\d+)/', 'manual_confirm', name='manual-confirm'),
)
