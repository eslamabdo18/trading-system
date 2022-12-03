from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserTransaction


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'balance',
    )


@admin.register(UserTransaction)
class UserTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stock',
                    'total_count', 'total_price', 'type')


admin.site.register(User, CustomUserAdmin)
