from django.contrib import admin

from vans.models import (Van, Status, Log)

class VanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'plates',
        'economic_number',
        'seats',
        'status',
        'created_at',
        'modified_at',
    )

class StatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
        'name',
    )

class LogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'van',
        'initial_status',
        'final_status',
        'created_at',
    )

#TODO: Add Admin (front) validations


admin.site.register(Van, VanAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Log, LogAdmin)