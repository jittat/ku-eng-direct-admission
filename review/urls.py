from django.conf.urls.defaults import *

urlpatterns = patterns(
    'review.views',

    url(r'^$', 'index', name='review-index'),
    url(r'^ticket/$', 'verify_ticket', name='review-ticket'),
    url(r'^search/$', 'search', name='review-search'),
    url(r'^show/(\d+)/$', 'review_document', name='review-show'),
    url(r'^show/(\d+)/manual/$', 'review_document', 
        { 'return_to_manual': True }, name='review-show-after-manual'),
    url(r'^received/toggle/(\d+)/$', 'toggle_received_status', 
        name='review-toggle-received-status'),
    url(r'^list/complete/$', 'list_applicant',
        { 'reviewed': True }, name='review-list-complete'),
    url(r'^list/wait/$', 'list_applicant',
        { 'reviewed': False }, name='review-list-wait'),
    url(r'^list/supplements/$', 'list_applicant_with_supplements',
        name='review-list-supplements'),
    url(r'^view/(\d+)/(\w+)/', 'doc_view', name='review-doc-view'),
    url(r'^supplement/view/(\w+)/', 
        'supplement_view', name='review-supplement-view'),
    url(r'^img/(\d+)/(\w*)', 'doc_img_view', name='review-doc-img-view'),
    url(r'^supplement/img/(\w*)', 'supplement_img_view', 
        name='review-supplement-img-view'),
)
