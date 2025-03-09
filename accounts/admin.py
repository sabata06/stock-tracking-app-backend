from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    This class uses Django's built-in UserAdmin to display
    our custom fields in the admin panel.
    """
    # Listede görünecek alanlar:
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    # Arama yapılacak alanlar:
    search_fields = ('email', 'first_name', 'last_name')
    # Kullanıcı oluştururken veya düzenlerken görünecek alanlar:
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    ordering = ('email',)
