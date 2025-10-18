from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TranslatorProfile, ClientProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_interpreter', 'is_client', 'is_moderator', 'is_staff')
    list_filter = ('is_interpreter', 'is_client', 'is_moderator', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('is_interpreter', 'is_moderator', 'is_client')
        }),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'phone_number')
    search_fields = ('user__username', 'firstname', 'lastname')

class TranslatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'translation_language')
    search_fields = ('user__username', 'region', 'translation_language')
    list_filter = ('region', 'translation_language')

class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization')
    search_fields = ('user__username', 'organization')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TranslatorProfile, TranslatorProfileAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)