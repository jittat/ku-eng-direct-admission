#!/usr/bin/env python
"""
run project with CherryPy wsgi server taken from
http://www.eflorenzano.com/blog/post/hosting-django-site-pure-python/
"""

from cherrypy import wsgiserver
import os
import sys
import django.core.handlers.wsgi

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    server = wsgiserver.CherryPyWSGIServer(
        ('0.0.0.0', 8000),
        django.core.handlers.wsgi.WSGIHandler(),
        server_name='www.django.example',
        numthreads = 20,
    )

    print 'started...'
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
