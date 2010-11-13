from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns(
    'application.views',

    url(r'^start/$', 'account.login', name='apply-start'),
    url(r'^login/$', 'account.login', name='apply-login'),
    url(r'^logout/$', 'account.logout', name='apply-logout'),
    url(r'^forget/$', 'account.forget_password', name='apply-forget'),
    url(r'^register/$', 'account.register', name='apply-register'),
    url(r'^activate/(\w+)/$', 'account.activate', name='apply-activate'),

    url(r'^personal/$', 'applicant_personal_info', name='apply-personal-info'),
    url(r'^address/$', 'applicant_address', name='apply-address'),
    url(r'^education/$', 'applicant_education', name='apply-edu'),
    url(r'^majors/$', 'applicant_major', name='apply-majors'),

    url(r'^confirm/$', 'info_confirm', name='apply-confirm'),

    url(r'^conditions/$', 'applicant_conditions', name='apply-conditions'),

    url(r'^ticket/$', 'submission_ticket', name='apply-ticket'),

    url(r'^incomplete/$', direct_to_template, 
        {'template': 'application/submission/incomplete_error.html'},
        name='apply-incomplete'),

    url(r'^status/$', 'status.index', name='status-index'),
    url(r'^status/show/$', 'status.show', name='status-show'),
    url(r'^status/ticket/$', 'status.show_ticket', name='status-show-ticket'),
    url(r'^status/request/$', 'status.request_status', name='status-request'),

    # update
    url(r'^update/majors/$', 'update.update_majors', name='update-majors'),
    url(r'^update/education/$', 'update.update_education', 
        name='update-education'),
    url(r'^update/postal_sub/$', 'update.update_to_postal_submission', 
        name='update-postal-sub'),

    # Example:
    # (r'^adm/', include('adm.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
               
)
