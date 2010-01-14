from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

media_pattern = settings.MEDIA_URL
if media_pattern[0]=='/':
    media_pattern = media_pattern[1:]

urlpatterns = patterns(
    '',
    url(r'^$', 'application.views.account.login', 
        name='start-page'),

    (r'^apply/', include('adm.application.urls')),
    (r'^doc/', include('adm.upload.urls')),
    (r'^review/', include('adm.review.urls')),
    (r'^manual/', include('adm.manual.urls')),
    (r'^supplement/', include('adm.supplement.urls')),
    (r'^result/', include('adm.result.urls')),
    (r'^confirm/', include('adm.confirmation.urls')),

    url(r'^deadline_passed/$', 
        'commons.views.deadline_passed_error',
        name='commons-deadline-error'),

    # authentication
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
     { 'next_page': settings.LOGOUT_URL }),

    # Example:
    # (r'^adm/', include('adm.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Static media (for development)
    (r'^'+ media_pattern +r'(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.STATIC_DOC_ROOT}),
)
