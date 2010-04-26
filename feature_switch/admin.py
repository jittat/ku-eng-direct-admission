from django.contrib import admin
from models import Feature

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'disabled')
    list_editable = ('disabled',)

admin.site.register(Feature, FeatureAdmin)
