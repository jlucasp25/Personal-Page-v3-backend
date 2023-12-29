from django.contrib import admin

from personal_page.core.models import Activity, Technology, Project, WorkCompany, CustomerCompany

# Register your models here.
admin.site.register(Activity)
admin.site.register(Technology)
admin.site.register(Project)
admin.site.register(WorkCompany)
admin.site.register(CustomerCompany)
