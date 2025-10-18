from django.contrib import admin
from .models import ContactUs, BookDemo

# Register the ContactUs model with the Django admin site.
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'last_name', 'email', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

# Register the BookDemo model with the Django admin site.
@admin.register(BookDemo)
class BookDemoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'organization', 'phone', 'created_at')
    list_filter = ('created_at', 'region')
    search_fields = ('first_name', 'last_name', 'email', 'organization', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)