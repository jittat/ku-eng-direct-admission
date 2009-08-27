from django.conf.urls.defaults import *

urlpatterns = patterns(
    'application.views',
    url(r'^start/$', 'start', name='apply-start'),
    url(r'^login/$', 'login', name='apply-login'),
    url(r'^core/$', 'applicant_core_info', name='apply-core'),
    url(r'^address/$', 'applicant_address', name='apply-address'),
    url(r'^education/$', 'applicant_education', name='apply-edu'),
    url(r'^majors/$', 'applicant_major', name='apply-majors'),

    url(r'^doc_menu/$', 'applicant_doc_menu', name='apply-doc-menu'),
    # Example:
    # (r'^adm/', include('adm.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
               
)
