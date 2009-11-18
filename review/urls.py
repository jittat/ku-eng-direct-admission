from django.conf.urls.defaults import *

urlpatterns = patterns(
    'review.views',

    url(r'^$', 'index', name='review-index'),
    url(r'^ticket/$', 'verify_ticket', name='review-ticket'),
    url(r'^received/toggle/(\d+)/$', 'toggle_received_status', 
        name='review-toggle-received-status'),
)
