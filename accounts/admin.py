from django.contrib import admin

from accounts.models import (User, RecoveryToken)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'created',
    )


class RecoveryTokenAdmin(admin.ModelAdmin):
    list_display = (
        'key',
        'expired',
        'expiration',
    )


admin.site.register(User, UserAdmin)
admin.site.register(RecoveryToken, RecoveryTokenAdmin)