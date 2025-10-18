import logging
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from django.http import HttpResponseRedirect
from .forms import TranslatorSignupForm, ClientSignupForm

logger = logging.getLogger(__name__)

class TranslatorSignupView(SignupView):
    form_class = TranslatorSignupForm
    template_name = 'account/translator_signup.html'
    
    def get_success_url(self):
        # Redirect to a page that tells user to check email
        return reverse_lazy('account_email_verification_sent')
    
    def form_valid(self, form):
        """Handle successful form submission"""
        try:
            form.save(self.request)
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            logger.error(f"Error in form submission: {str(e)}")
            form.add_error(None, str(e))
            return self.form_invalid(form)
        
    def form_invalid(self, form):   
        """Handle form validation errors"""
        for field, errors in form.errors.items():
            for error in errors:
                error_msg = str(error)  # Convert proxy object to string
                messages.error(self.request, f"{field}: {error_msg}")
        return super().form_invalid(form)


class ClientSignupView(SignupView):
    form_class = ClientSignupForm
    template_name = 'account/client_signup.html'
    
    def get_success_url(self):
        # Redirect to a login page
        return reverse_lazy('account_login')
        
    def form_valid(self, form):
        """Handle successful form submission"""
        try:
            form.save(self.request)
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            logger.error(f"Error in form submission: {str(e)}")
            form.add_error(None, str(e))
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        """Handle form validation errors"""
        for field, errors in form.errors.items():
            for error in errors:
                error_msg = str(error)  # Convert proxy object to string
                messages.error(self.request, f"{field}: {error_msg}")
        return super().form_invalid(form)

def account_type_choice(request):
    """View to let users choose their signup type"""
    return render(request, 'account/account_type.html')