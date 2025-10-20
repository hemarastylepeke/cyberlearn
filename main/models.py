from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Get the user model
User = get_user_model()

# Contact Us model.
class ContactUs(models.Model):
    """
    Model to store contact us form submissions.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.first_name} at {self.email}"

# Notes model  
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

# Book Demo Model.
class BookDemo(models.Model):
    """
    Model to store book demo form submissions with status tracking and interpreter assignment.
    """
    # Status choices
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('completed', 'completed'),
    ]
    
    # Original fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='demo_bookings', help_text="The user who submitted this demo request (if authenticated)")
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    organization = models.CharField(max_length=200, blank=False, null=True)
    phone = models.CharField(max_length=15, blank=False, null=True)
    region = models.CharField(max_length=100, blank=False, null=True)
    message = models.TextField(blank=False, null=False)
    how_did_you_hear = models.CharField(max_length=200, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',help_text="Current status of the booking")
    assigned_interpreter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_interpreter': True, 'translatorprofile__is_approved': True}, related_name='assigned_bookings', help_text="The interpreter assigned to handle this booking")
    scheduled_date = models.DateTimeField(null=True, blank=True,help_text="When the demo/interpretation is scheduled")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, help_text="Expected duration of the session in minutes")
    assigned_at = models.DateTimeField(null=True, blank=True,help_text="When the interpreter was assigned")
    completed_at = models.DateTimeField(null=True, blank=True,help_text="When the booking was marked as completed")
    admin_notes = models.TextField(blank=True, null=True,help_text="Internal notes for administrators")
    required_language = models.CharField(max_length=100,  blank=True, null=True,help_text="Language required for interpretation")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Demo Booking"
        verbose_name_plural = "Demo Bookings"
    
    def __str__(self):
        return f"Demo booking from {self.first_name} {self.last_name}"