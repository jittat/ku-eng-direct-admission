from django.contrib import admin
from models import ReviewField

class ReviewFieldAdmin(admin.ModelAdmin):
    list_display = ['name','short_name','order','required']
    list_editable = ['short_name','order']

admin.site.register(ReviewField, ReviewFieldAdmin)
