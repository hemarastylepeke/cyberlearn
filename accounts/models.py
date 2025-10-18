from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    is_interpreter = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username

class BaseProfile(models.Model):
    """Abstract base profile with common fields"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    
    class Meta:
        abstract = True

class TranslatorProfile(BaseProfile):
    """Complete profile for translators - includes base fields + translator-specific"""
    region = models.CharField(max_length=100)
    translation_language = models.CharField(max_length=100)
    cv = models.FileField(upload_to="translator_cvs/", null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Translator Profile of {self.user.email}"

class ClientProfile(BaseProfile):
    """Complete profile for clients - includes base fields + client-specific"""
    organization = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Client Profile of {self.user.email}"
    
class ModeratorProfile(BaseProfile):
    """Complete profile for moderators - includes base fields + moderators-specific"""
    # Other fields specific to moderators can be added here
    
    def __str__(self):
        return f"Client Profile of {self.user.email}"