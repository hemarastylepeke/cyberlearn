from django import forms
from .models import Note
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

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Note title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Write your note here...',
                'rows': 12,
            }),
        }