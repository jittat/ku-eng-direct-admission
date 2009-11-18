from django.conf.urls.defaults import *

urlpatterns = patterns(
    'review.views',

    url(r'^$', 'index', name='review-index'),
)
