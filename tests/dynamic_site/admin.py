from django.contrib import admin

from tests.dynamic_site import models

admin.site.site_header = 'Dynamic Site'
admin.site.site_title = 'Dynamic Site'


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin[models.User]):
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser']


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin[models.Project]):
    date_hierarchy = 'start_date'
    list_display = ['id', 'name', 'start_date', 'end_date', 'status']
    fields = ['name', ('start_date', 'end_date'), 'status']
    list_filter = ['status', 'start_date', 'end_date']
    search_fields = ['id', 'name', 'status']
    search_help_text = 'Search by ID, name or status'
