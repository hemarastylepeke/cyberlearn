from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # Allauth URLs for authentication
    path('accounts/', include('accounts.urls')), # Custom signup and account type selection URLs
]
