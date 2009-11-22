"""
This is a migration for django-mailer, to add indices for email search
in message logs.

This is just a HACK.

It is kept here, so that we do not have to change the implementation
of django-mailer.
"""
from south.db import db
from django.db import models
from adm.commons.models import *

class Migration:
    
    def forwards(self, orm):
        "create to_address index for django-mailer"
        try:
            from mailer.models import MessageLog
            db.create_index('mailer_messagelog',['to_address'])
        except:
            print "No MessageLog"
            pass
    
    
    def backwards(self, orm):
        try:
            from mailer.models import MessageLog
            db.delete_index('mailer_messagelog',['to_address'])
        except:
            print "No MessageLog"
            pass
    
    
    
    models = {
        
    }
    
    complete_apps = ['commons']
