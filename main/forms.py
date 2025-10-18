from django import forms
from .models import ContactUs, BookDemo

class ContactForm(forms.ModelForm):
    """
    Form for handling contact submissions
    """
    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']


class BookDemoForm(forms.ModelForm):
    """
    Form for handling demo booking submissions
    """
    class Meta:
        model = BookDemo 
        fields = ['first_name', 'last_name', 'email', 'organization', 'phone', 'region', 'message', 'how_did_you_hear']