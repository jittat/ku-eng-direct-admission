from django.contrib import admin
from models import Applicant, SubmissionInfo, PersonalInfo
from models import Address, ApplicantAddress
from models import Education, Major, GPExamDate

admin.site.register(SubmissionInfo)
admin.site.register(PersonalInfo)
admin.site.register(Address)
admin.site.register(GPExamDate)
admin.site.register(Education)
admin.site.register(Major)
admin.site.register(ApplicantAddress)

class PersonalInfoInline(admin.StackedInline):
    model = PersonalInfo

class ApplicantAdmin(admin.ModelAdmin):
    exclude = ('has_related_model',)

    list_display = ['full_name', 'email']
    search_fields = ['email']

    inlines = [
        PersonalInfoInline,
        ]

admin.site.register(Applicant, ApplicantAdmin)

