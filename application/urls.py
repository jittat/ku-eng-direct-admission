from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns(
    'application.views',

    url(r'^start/$', direct_to_template,
        {'template': 'application/start.html'}, 
        name='apply-start'),
    url(r'^login/$', 'login', name='apply-login'),
    url(r'^logout/$', 'logout', name='apply-logout'),
    url(r'^forget/$', 'forget_password', name='apply-forget'),

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
