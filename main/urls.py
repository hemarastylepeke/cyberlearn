from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('profile/', views.profile, name='profile'),
    path('privacy/', views.privacy, name='privacy'),
    path('refundpolicy/', views.refundpolicy, name='refundpolicy'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('submit-project/', views.bookdemo, name='submit_project'),
    path('languages/', views.languages, name='languages'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assignedbookings/', views.interpreter_assigned_bookings, name='interpreter_assigned_bookings'),

    # Admin urls
    path('manageclients/', views.manageclients, name='manageclients'),
    path('bookings/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('clients/<int:client_id>/delete/', views.delete_client, name='delete_client'),
    path('bookings/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('admin_manage_bookings/', views.admin_manage_bookings, name='admin_manage_bookings'),
    path('adminmanageinterpreters/', views.adminmanageinterpreters, name='adminmanageinterpreters'),
    path('messages/<int:message_id>/delete/', views.admin_delete_message, name='admin_delete_message'),
    path('clients/<int:client_id>/', views.admin_manage_client_detail, name='admin_manage_client_detail'),
    path('interpreters/<int:interpreter_id>/delete/', views.delete_interpreter, name='delete_interpreter'),
    path('clients/<int:client_id>/toggle-status/', views.toggle_client_status, name='toggle_client_status'),
    path('admin/contact-messages/', views.admin_manage_contact_messages, name='admin_manage_contact_messages'),
    path('interpreter/<int:interpreter_id>/approve/', views.admin_approve_interpreter, name='admin_approve_interpreter'),
    path('interpreter/<int:interpreter_id>/', views.admin_manage_interpreter_detail, name='admin_manage_interpreter_detail'),
    path('admin/contact-messages/<int:message_id>/', views.admin_contact_message_detail, name='admin_contact_message_detail'),
    path('interpreters/<int:interpreter_id>/toggle-status/', views.toggle_interpreter_status, name='toggle_interpreter_status'),

    # Notes urls
    path('notes/add/', views.add_note, name='add_note'),
    path('notes/', views.all_notes, name='all_notes'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('notes/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]