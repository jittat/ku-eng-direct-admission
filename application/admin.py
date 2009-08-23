from django.contrib import admin
from models import Applicant, Address, ApplicantAddress

admin.site.register(Applicant)
admin.site.register(Address)
admin.site.register(ApplicantAddress)
