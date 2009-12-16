from django.contrib import admin
from models import SupplementType, Supplement

admin.site.register(Supplement)

class SupplementTypeAdmin(admin.ModelAdmin):
    list_display = ['name','order']
    list_editable = ['order']

admin.site.register(SupplementType, SupplementTypeAdmin)
