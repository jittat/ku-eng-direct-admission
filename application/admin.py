from django.contrib import admin
from models import Applicant, Address, ApplicantAddress, Education

admin.site.register(Applicant)
admin.site.register(Address)
admin.site.register(ApplicantAddress)
admin.site.register(Education)
