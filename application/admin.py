from django.contrib import admin
from models import Applicant, SubmissionInfo, PersonalInfo
from models import Address, ApplicantAddress
from models import Education, Major, GPExamDate

class ApplicantAdmin(admin.ModelAdmin):
    exclude = ('has_related_model',)

admin.site.register(Applicant, ApplicantAdmin)

admin.site.register(SubmissionInfo)
admin.site.register(PersonalInfo)
admin.site.register(Address)
admin.site.register(ApplicantAddress)
admin.site.register(GPExamDate)
admin.site.register(Education)
admin.site.register(Major)
