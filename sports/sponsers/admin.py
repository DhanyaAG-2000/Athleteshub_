from django.contrib import admin

# Register your models here.

from .models import SponsorCompany,SponsorshipRequest


admin.site.register(SponsorCompany)
admin.site.register(SponsorshipRequest)