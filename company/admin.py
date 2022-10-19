from django.contrib import admin

from company.models import CompanyModel,ReportingEntityModel

# Register your models here.

admin.site.register(ReportingEntityModel)
admin.site.register(CompanyModel)