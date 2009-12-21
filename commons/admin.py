from django.contrib import admin
from models import Announcement, Log

class AnnouncementAdmin(admin.ModelAdmin):
    fields = ('body', 'is_enabled', 'created_at')

admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Log)
