from django.conf.urls.defaults import *

urlpatterns = patterns(
    'application.views',
    url(r'^start/$', 'applicant_core_info', name='apply-start'),
    # Example:
    # (r'^adm/', include('adm.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
               
)
