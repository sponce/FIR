from django.contrib import admin

from fir_siem.models import SIEMCase, Email

admin.site.register(SIEMCase)
admin.site.register(Email)
