from django.urls import path
from . import views

urlpatterns = [
    path('signup/client/', views.ClientSignupView.as_view(), name='clientsignup'),
    path('account_type_choice/', views.account_type_choice, name='account_type_choice'),
    path('signup/translator/', views.TranslatorSignupView.as_view(), name='translatorsignup'),
]