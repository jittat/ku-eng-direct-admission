
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
