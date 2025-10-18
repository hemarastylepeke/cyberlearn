# forms.py
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import TranslatorProfile, ClientProfile
from allauth.account.forms import SignupForm, LoginForm
from allauth.core.exceptions import ImmediateHttpResponse

User = get_user_model()

class TranslatorSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    region = forms.CharField(max_length=100, required=True)
    translation_language = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    profile_photo = forms.ImageField(required=False)
    cv = forms.FileField(required=False)

    def save(self, request):
        # Call parent save method which handles email verification
        user = super().save(request)
        
        # Set user fields
        user.is_interpreter = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        # Create TranslatorProfile (includes all BaseProfile fields)
        translator_profile = TranslatorProfile.objects.create(
            user=user,
            firstname=self.cleaned_data['first_name'],
            lastname=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone'],
            profile_image=self.cleaned_data.get('profile_photo'),
            region=self.cleaned_data['region'],
            translation_language=self.cleaned_data['translation_language'],
            cv=self.cleaned_data.get('cv')
        )
        print(f"TranslatorProfile created: {translator_profile}")
        
        return user

class ClientSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=True)
    organization = forms.CharField(max_length=200, required=True)

    def save(self, request):
        # Call parent save method which handles email verification
        user = super().save(request)
        
        # Set user fields
        user.is_client = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        # Create ClientProfile (includes all BaseProfile fields)
        client_profile = ClientProfile.objects.create(
            user=user,
            firstname=self.cleaned_data['first_name'],
            lastname=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone'],
            organization=self.cleaned_data['organization']
        )
        return user
    
class CustomLoginForm(LoginForm):
    def login(self, request, redirect_url=None):
        try:
            # Store the request for use in error handling
            self.request = request
            
            # Check if user exists and account is active before attempting login
            login_field = self.cleaned_data.get("login")
            password = self.cleaned_data.get("password")
            
            if login_field and password:
                # Try to authenticate to check for specific error conditions
                user = authenticate(request, username=login_field, password=password)
                if user is None:
                    messages.error(request, "Invalid login credentials. Please try again.")
                elif not user.is_active:
                    messages.error(request, "Your account is inactive. Please contact support.")
            
            # Call the original login method
            ret = super().login(request, redirect_url)
            
            # If we get here, login was successful
            messages.success(request, f"Welcome back, {self.user.get_full_name() or self.user.username}!")
            
            return ret
            
        except ImmediateHttpResponse:
            # This exception is raised by allauth for various login issues
            if hasattr(self, 'user') and self.user and not self.user.is_active:
                messages.error(request, "Your account is not active.")
            elif not getattr(self, 'user', None):
                messages.error(request, "Invalid login credentials.")
            else:
                messages.error(request, "Login failed. Please try again.")
            # Re-raise to maintain allauth's flow
            raise
            
        except Exception as e:
            # Catch any other login-related errors
            messages.error(request, "An unexpected error occurred during login. Please try again.")
            raise

    def clean(self):
        # Override clean method to add custom validation messages
        try:
            cleaned_data = super().clean()
            return cleaned_data
        except forms.ValidationError as e:
            # Add error messages for form validation failures
            if hasattr(self, 'request'):
                messages.error(self.request, "Authentication failed, please try again!")
            raise