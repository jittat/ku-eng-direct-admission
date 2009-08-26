from django.contrib import admin
from models import Applicant, ApplicantAccount
from models import Address, ApplicantAddress
from models import Education, Major, GPExamDate

admin.site.register(Applicant)
admin.site.register(Address)
admin.site.register(ApplicantAddress)
admin.site.register(GPExamDate)
admin.site.register(Education)
admin.site.register(Major)
