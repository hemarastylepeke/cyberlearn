from accounts.models import CustomUser, ClientProfile, TranslatorProfile, ModeratorProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, BookDemoForm, NoteForm
from .models import BookDemo, ContactUs, Note
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone


@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('dashboard')
    else:
        form = NoteForm()
    
    return render(request, 'main/add_note.html', {'form': form})

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    return render(request, 'main/note_detail.html', {'note': note})

@login_required
def all_notes(request):
    notes = request.user.notes.all()
    return render(request, 'main/client_notes.html', {'notes': notes})

@login_required
@require_http_methods(["POST"])
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('all_notes')

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', note_id=note.id)
    else:
        form = NoteForm(instance=note)
    
    return render(request, 'main/add_note.html', {'form': form, 'note': note})

def refundpolicy(request):
    """
    Render the refund policy page.
    """
    return render(request, 'main/refundpolicy.html')

def home(request):
    """
    Render the home page.
    """
    return render(request, 'main/home.html')

def about(request):
    """
    Render the about page.
    """
    return render(request, 'main/about.html')

def contact(request):
    """
    Handle contact form submission and render the contact page.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'contact_form': form})

def services(request):
    """
    Render the services page.
    """
    return render(request, 'main/services.html')

def languages(request):
    """
    Render the languages page.
    """
    return render(request, 'main/languages.html')

def terms(request):
    """
    Render the terms page.
    """
    return render(request, 'main/terms.html')

def privacy(request):
    """
    Render the privacy policy page.
    """
    return render(request, 'main/privacy.html')

# views.py
@login_required(login_url='account_login')
def bookdemo(request):
    """
    Handle book demo form submission and render the Book Demo page.
    """
    if request.method == 'POST':
        form = BookDemoForm(request.POST)
        if form.is_valid():
            # Save form but don't commit to database yet
            demo_booking = form.save(commit=False)
            
            # Check if user is authenticated and associate with user
            if request.user.is_authenticated:
                demo_booking.user = request.user
            
                # Now save to database
                demo_booking.save()
                
                messages.success(request, 'Thank you for your message! We will get back to you soon!')
                return redirect('dashboard')
            else:
                form.save()
                messages.success(request, 'Thank you for your message! We will get back to you soon!')
                return redirect('bookdemo')
        else:
            messages.error(request, 'An error occured! Fill all fields and try again!')
    else:
        form = BookDemoForm()
    
    return render(request, 'main/submit_project.html', {'book_demo_form': form})

@login_required(login_url='account_login')
def dashboard(request):
    """
    Render the dashboard page with role-specific data.
    """
    context = {}
    user = request.user
    notes = request.user.notes.all()
    
    # Common data for all users
    context['user'] = user
    
    if user.is_interpreter:
        # Interpreter-specific data
        try:
            translator_profile = user.translatorprofile
            context['translator_profile'] = translator_profile
            
            # Get bookings assigned to this interpreter
            assigned_bookings = BookDemo.objects.filter(assigned_interpreter=user)
            context['assigned_bookings_count'] = assigned_bookings.count()
            context['completed_bookings_count'] = assigned_bookings.filter(status='completed').count()
            context['pending_bookings_count'] = assigned_bookings.filter(status='pending').count()
            
            # Recent bookings for this interpreter
            context['recent_bookings'] = assigned_bookings.order_by('-created_at')[:5]
            
        except TranslatorProfile.DoesNotExist:
            context['translator_profile'] = None
            context['assigned_bookings_count'] = 0
            context['completed_bookings_count'] = 0
            context['pending_bookings_count'] = 0
            context['recent_bookings'] = []
    
    elif user.is_moderator:
        # Moderator-specific data
        context['total_bookings_count'] = BookDemo.objects.count()
        context['active_interpreters_count'] = CustomUser.objects.filter(
            is_interpreter=True, 
            translatorprofile__is_approved=True
        ).count()
        context['pending_approvals_count'] = TranslatorProfile.objects.filter(
            is_approved=False
        ).count()
        context['contact_messages_count'] = ContactUs.objects.count()
        
        # Recent bookings for moderator view
        context['recent_bookings'] = BookDemo.objects.order_by('-created_at')[:5]
        
        # Recent contact messages
        context['recent_contacts'] = ContactUs.objects.order_by('-created_at')[:5]
    
    elif user.is_client:
        # Client-specific data
        try:
            client_profile = user.clientprofile
            context['client_profile'] = client_profile
        except:
            context['client_profile'] = None
        
        # Get bookings made by this client (assuming email matching)
        user_bookings = BookDemo.objects.filter(email=user.email)
        context['user_bookings_count'] = user_bookings.count()
        context['recent_bookings'] = user_bookings.order_by('-created_at')[:5]
    
    else:
        # General user (not assigned specific role yet)
        user_bookings = BookDemo.objects.filter(email=user.email)
        context['user_bookings_count'] = user_bookings.count()
        context['recent_bookings'] = user_bookings.order_by('-created_at')[:5]
    
    return render(request, 'main/dashboard.html', {'notes': notes})


@login_required(login_url='account_login')
def manageclients(request):
    """
    Render the page for the admins to manage clients.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to view this page.')
        return redirect('dashboard')
    
    # Get clients
    clients_with_profiles = CustomUser.objects.filter(is_client=True).prefetch_related('clientprofile')
    
    context = {
        'clients': clients_with_profiles,
    }
    
    return render(request, 'main/manage_clients.html', context)

@login_required(login_url='account_login')
def admin_manage_client_detail(request, client_id):
    """
    Render the detailed page for a specific client.
    Only accessible by moderators.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to view this page.')
        return redirect('dashboard')
    client = get_object_or_404(CustomUser, id=client_id, is_client=True)
    try:
        client_profile = ClientProfile.objects.get(user=client)
    except ClientProfile.DoesNotExist:
        client_profile = None
    
    context = {
        'client': client,
        'client_profile': client_profile,
    }
    return render(request, 'main/admin_manage_client_detail.html', context)

@login_required(login_url='account_login')
def delete_client(request, client_id):
    """
    Delete a client account.
    Only accessible by moderators via POST request.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        client = get_object_or_404(CustomUser, id=client_id, is_client=True)
        client_username = client.username

        client.delete()
        
        messages.success(request, f'Client {client_username} has been deleted successfully.')
        return redirect('manageclients')
    return redirect('client_detail', client_id=client_id)

@login_required(login_url='account_login')
def toggle_client_status(request, client_id):
    """
    Toggle the active status of a client (activate/deactivate).
    Only accessible by moderators via POST request.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        client = get_object_or_404(CustomUser, id=client_id, is_client=True)

        client.is_active = not client.is_active
        client.save()
        
        status = "activated" if client.is_active else "deactivated"
        messages.success(request, f'Client {client.username} has been {status} successfully.')
    return redirect('admin_manage_client_detail', client_id=client_id)

@login_required(login_url='account_login')
def adminmanageinterpreters(request):
    """
    Render the page for the admins to manage interpreters.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to view this page.')
        return redirect('dashboard')
    
    # Get Interpreters
    interpreters_with_profiles = CustomUser.objects.filter(is_interpreter=True).prefetch_related('translatorprofile')
    
    # Count approved and unapproved interpreters using the related field
    approved_count = interpreters_with_profiles.filter(translatorprofile__is_approved=True).count()
    unapproved_count = interpreters_with_profiles.filter(translatorprofile__is_approved=False).count()
    total_count = interpreters_with_profiles.count()
    
    context = {
        'interpreters': interpreters_with_profiles,
        'approved_count': approved_count,
        'unapproved_count': unapproved_count,
        'total_count': total_count,
    }
    return render(request, 'main/admin_manage_interpreters.html', context)

@login_required(login_url='account_login')
def admin_manage_interpreter_detail(request, interpreter_id):
    """
    Render the detailed page for a specific interpreter.
    Only accessible by moderators.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to view this page.')
        return redirect('dashboard')
    interpreter = get_object_or_404(CustomUser, id=interpreter_id, is_interpreter=True)
    try:
        interpreter_profile = TranslatorProfile.objects.get(user=interpreter)
    except TranslatorProfile.DoesNotExist:
        interpreter_profile = None
    
    context = {
        'interpreter': interpreter,
        'interpreter_profile': interpreter_profile,
    }
    return render(request, 'main/admin_manage_interpreter_detail.html', context)


@login_required(login_url='account_login')
def toggle_interpreter_status(request, interpreter_id):
    """
    Toggle the active status of a interpreter (activate/deactivate).
    Only accessible by moderators via POST request.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        interpreter = get_object_or_404(CustomUser, id=interpreter_id, is_interpreter=True)

        interpreter.is_active = not interpreter.is_active
        interpreter.save()
        
        status = "activated" if interpreter.is_active else "deactivated"
        messages.success(request, f'Interpreter {interpreter.username} has been {status} successfully.')
    return redirect('admin_manage_interpreter_detail', interpreter_id=interpreter_id)

@login_required(login_url='account_login')
def delete_interpreter(request, interpreter_id):
    """
    Delete a interpreter account.
    Only accessible by moderators via POST request.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        interpreter = get_object_or_404(CustomUser, id=interpreter_id, is_interpreter=True)
        interpreter_username = interpreter.username

        interpreter.delete()
        
        messages.success(request, f'Interpreter {interpreter_username} has been deleted successfully.')
        return redirect('adminmanageinterpreters')
    return redirect('interpreter_detail', interpreter_id=interpreter_id)

@login_required(login_url='account_login')
def admin_approve_interpreter(request, interpreter_id):
    """
    Admin to be able to approve interpreter.
    Only accessible by moderators via POST request.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        interpreter = get_object_or_404(CustomUser, id=interpreter_id, is_interpreter=True)
        try:
            translator_profile = interpreter.translatorprofile
            translator_profile.is_approved = not translator_profile.is_approved
            translator_profile.save()

            status = "approved" if translator_profile.is_approved else "unapproved"
            messages.success(request, f'Interpreter {interpreter.username} has been {status} successfully.')
        except TranslatorProfile.DoesNotExist:
            messages.error(request, f'Interpreter {interpreter.username} does not have a complete profile.')
    return redirect('admin_manage_interpreter_detail', interpreter_id=interpreter_id)

@login_required(login_url='account_login')
def admin_manage_bookings(request):
    """
    Admin to be able to manage client bookings.
    Only accessible by moderators.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    # Get all bookings with related interpreter data
    bookings = BookDemo.objects.select_related().all()
    
    # Get booking statistics
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='pending').count()
    completed_bookings = bookings.filter(status='completed').count()
    assigned_bookings = bookings.filter(assigned_interpreter__isnull=False).count()
    unassigned_bookings = bookings.filter(assigned_interpreter__isnull=True).count()
    
    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'assigned_bookings': assigned_bookings,
        'unassigned_bookings': unassigned_bookings,
    }
    
    return render(request, 'main/admin_manage_bookings.html', context)


@login_required(login_url='account_login')
def booking_details(request, booking_id):
    """
    Admin view to display detailed information about a specific booking.
    Only accessible by moderators.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    # Get the specific booking or return 404 if not found
    booking = get_object_or_404(BookDemo.objects.select_related(), id=booking_id)
    
    if request.method == 'POST':
        # Handle form submission
        status = request.POST.get('status')
        interpreter_id = request.POST.get('assigned_interpreter')
        scheduled_date = request.POST.get('scheduled_date')
        duration_minutes = request.POST.get('duration_minutes')
        admin_notes = request.POST.get('admin_notes')
        required_language = request.POST.get('required_language')

        # Update status and completion time
        if status and status in dict(booking.STATUS_CHOICES):
            booking.status = status
            if status == 'completed' and not booking.completed_at:
                booking.completed_at = timezone.now()

        # Update interpreter
        if interpreter_id:
            interpreter = get_object_or_404(CustomUser, id=interpreter_id)
            if interpreter != booking.assigned_interpreter:
                booking.assigned_interpreter = interpreter
                booking.assigned_at = timezone.now()
        
        # Update other fields
        if scheduled_date:
            try:
                booking.scheduled_date = timezone.datetime.strptime(scheduled_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                messages.error(request, 'Invalid date format')
                return redirect('booking_details', booking_id=booking_id)

        if duration_minutes:
            try:
                booking.duration_minutes = int(duration_minutes)
            except ValueError:
                messages.error(request, 'Invalid duration format')
                return redirect('booking_details', booking_id=booking_id)

        booking.admin_notes = admin_notes if admin_notes else booking.admin_notes
        booking.required_language = required_language if required_language else booking.required_language

        booking.save()
        messages.success(request, 'Booking details updated successfully.')
        return redirect('booking_details', booking_id=booking_id)
    
    # Get list of interpreters for the form
    interpreters_with_profiles = CustomUser.objects.filter(is_interpreter=True, translatorprofile__is_approved=True).prefetch_related('translatorprofile')
    
    context = {
        'booking': booking,
        'interpreters': interpreters_with_profiles
    }
    
    return render(request, 'main/booking_details.html', context)


@login_required(login_url='account_login')
def delete_booking(request, booking_id):
    """
    Delete the booking.
    Only accessible by moderators via POST request.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        booking = get_object_or_404(BookDemo, id=booking_id)
        # Store info for success message before deletion
        client_name = f"{booking.first_name} {booking.last_name}"
        
        # Delete the booking
        booking.delete()
        
        messages.success(request, f'Booking from {client_name} has been deleted successfully.')
        return redirect('admin_manage_bookings')
        
    return redirect('booking_details', booking_id=booking_id)

@login_required(login_url='account_login')
def admin_manage_contact_messages(request):
    """
    Admin to be able to manage contact us messages.
    Only accessible by moderators.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    # Get all contact messages ordered by newest first
    contact_messages = ContactUs.objects.all().order_by('-created_at')
    
    # Get contact message statistics
    total_messages = contact_messages.count()
    today_messages = contact_messages.filter(created_at__date=timezone.now().date())
    
    context = {
        'total_messages': total_messages,
        'today_messages': today_messages,
        'contact_messages': contact_messages
    }
    
    return render(request, 'main/admin_manage_contact_messages.html', context)

@login_required(login_url='account_login')
def admin_contact_message_detail(request, message_id):
    """
    Admin to view detailed contact us message.
    Only accessible by moderators.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    # Get the specific contact message or return 404
    contact_message = get_object_or_404(ContactUs, id=message_id)
    
    context = {
        'contact_message': contact_message,
    }
    
    return render(request, 'main/admin_contact_message_detail.html', context)


@login_required(login_url='account_login')
def admin_delete_message(request, message_id):
    """
    Delete the message.
    Only accessible by moderators via POST request.
    """
    if not hasattr(request.user, 'is_moderator') or not request.user.is_moderator:
        messages.error(request, 'Access denied. You must be a moderator to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        message = get_object_or_404(ContactUs, id=message_id)
        # Store info for success message before deletion
        client_name = f"{message.first_name} {message.last_name}"
        
        # Delete the booking
        message.delete()
        
        messages.success(request, f'Message from {client_name} has been deleted successfully.')
        return redirect('admin_manage_contact_messages')
        
    return redirect('booking_details', message_id=message_id)


@login_required(login_url='account_login')
def profile(request):
    """
        View to get user profile.
        Only accessible by authenticated users.
    """
    user = request.user
    profile = None
    profile_type = None
    
    # Determine which profile to fetch based on user type
    try:
        if user.is_interpreter:
            profile = TranslatorProfile.objects.get(user=user)
            profile_type = 'translator'
        elif user.is_client:
            profile = ClientProfile.objects.get(user=user)
            profile_type = 'client'
        elif user.is_moderator:
            profile = ModeratorProfile.objects.get(user=user)
            profile_type = 'moderator'
    except (TranslatorProfile.DoesNotExist, ClientProfile.DoesNotExist, ModeratorProfile.DoesNotExist):
        profile = None
    
    context = {
        'user': user,
        'profile': profile,
        'profile_type': profile_type,
    }
    
    return render(request, 'main/profile.html', context)

@login_required(login_url='account_login')
def interpreter_assigned_bookings(request):
    """
    Interpreter to be able to view their assigned bookings.
    Only accessible by users who are interpreters.
    """
    # Check if the current user is an interpreter
    if not request.user.is_interpreter:
        messages.error(request, 'Access denied. Only interpreters can view this page.')
        return redirect('profile')  # or wherever you want to redirect
    
    # Get bookings assigned to the current interpreter
    assigned_bookings = BookDemo.objects.filter(assigned_interpreter=request.user).order_by('-created_at')
    
    # Get booking statistics for the interpreter
    total_assigned = assigned_bookings.count()
    pending_assigned = assigned_bookings.filter(status='pending').count()
    completed_assigned = assigned_bookings.filter(status='completed').count()
    
    # Get bookings by status for better organization
    pending_bookings = assigned_bookings.filter(status='pending')
    completed_bookings = assigned_bookings.filter(status='completed')
    
    # Get recent assignments (last 5)
    recent_assignments = assigned_bookings[:5]
    
    # Get upcoming scheduled bookings (if scheduled_date is set and in the future)
    from django.utils import timezone
    upcoming_bookings = assigned_bookings.filter(scheduled_date__gte=timezone.now(), status='pending').order_by('scheduled_date')
    
    context = {
        'assigned_bookings': assigned_bookings,
        'total_assigned': total_assigned,
        'pending_assigned': pending_assigned,
        'completed_assigned': completed_assigned,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'recent_assignments': recent_assignments,
        'upcoming_bookings': upcoming_bookings,
        'interpreter': request.user,
    }
    
    return render(request, 'main/interpreter_assigned_bookings.html', context)

