
from django.views.generic import View
from django.shortcuts import render, redirect,get_object_or_404
from atheletes.models import Users
from events.models import SportsEvent
from django.db.models import Q
from .forms import EventRegistrationForm
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .utility import send_email,registration_fees  # Make sure this exists and works properly
from .models import ProfileDetails,EventWinner  # Replace with your actual model
from datetime import date
from sponsers.models import SponsorCompany
from django.views import View

from sponsers.models import SponsorCompany
from .models import EventWinner
from events.models import SportsEvent
from payments.models import Payment

  # Assuming you meant this as the participant data model






class StudentView(View):
    def get(self, request, *args, **kwargs):
        user_details = Users.objects.filter(profile=request.user).first()
        return render(request, 'students/students-view.html', {'user_details': user_details})


class GetUserObject:


    def get_user(self,request,uuid):

        try :

            user = Users.objects.get(uuid=uuid)

            return user
        
        except :

            return render(request,"error/error-404.html")
        
 

class ApplyEventsview(View):

     def get(self, request, *args, **kwargs):

        search_query = request.GET.get('search', '')

        events = SportsEvent.objects.all()
        
        if search_query:
            events = events.filter(
                Q(title__icontains=search_query) |   
                Q(sport_type__icontains=search_query) |
                Q(venue__icontains=search_query) |
                Q(district__icontains=search_query)|
                Q(reg_number__icontains=search_query)|
                Q(sport_type__icontains=search_query)
            )

        return render(request, 'students/student-apply-events.html', {

            'events': events,

            'search_query': search_query

        })


class RegisteredListView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        date_filter = request.GET.get('date', '')
        registrations = ProfileDetails.objects.all()

        if query:
            registrations = registrations.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(reg_number__icontains=query) |
                Q(title__title__icontains=query) |
                Q(category__icontains=query) |
                Q(institution__icontains=query)|
                Q(first_name__icontains=query) &
                Q(last_name__icontains=query) 
            )
        if date_filter:
            registrations = registrations.filter(created_at__date=date_filter)

        return render(request, 'students/registered-event-list.html', {
            'registrations': registrations,
            'query': query,
            'date_filter': date_filter,
        })



       
class WinnersListView(View):
    def get(self, request, *args, **kwargs):
        print(request.META)  # Add this line to debug the request object
        winners = EventWinner.objects.select_related('registered_event')
        return render(request, 'winners/winners-list.html', {'winners': winners})


class AssignWinnersView(View):
    def get(self, request, *args, **kwargs):
        events = SportsEvent.objects.all()
        selected_event_id = request.GET.get('event')
        participants = []
        selected_event = None

        if selected_event_id:
            try:
                selected_event = SportsEvent.objects.get(id=selected_event_id)
                participants = ProfileDetails.objects.filter(title=selected_event).order_by('first_name')
            except SportsEvent.DoesNotExist:
                messages.error(request, "Selected event does not exist.")

        context = {
            'events': events,
            'participants': participants,
            'selected_event': selected_event.id if selected_event else None,
        }
        return render(request, 'winners/assign-winners.html', context)

    def post(self, request, *args, **kwargs):
        selected_event_id = request.POST.get('event')
        reg_numbers = request.POST.getlist('reg_number[]')
        positions = request.POST.getlist('winner_position[]')

        if not selected_event_id or not reg_numbers:
            messages.error(request, "Please select an event and assign at least one winner.")
            return redirect('assign-winners')

        try:
            event = SportsEvent.objects.get(id=selected_event_id)
        except SportsEvent.DoesNotExist:
            messages.error(request, "Selected event does not exist.")
            return redirect('assign-winners')

        for reg_number, pos in zip(reg_numbers, positions):
            if not pos:
                continue

            reg = ProfileDetails.objects.filter(reg_number=reg_number, title=event).first()
            if not reg:
                continue

            # Check if this position is already assigned
            if EventWinner.objects.filter(registered_event=event, position=pos).exists():
                messages.error(request, f"{pos} place is already assigned for this event.")
                continue

            # Save the winner
            EventWinner.objects.create(
                first_name=reg.first_name,
                last_name=reg.last_name,
                registered_event=event,
                institution=reg.institution,
                category=reg.category,
                university=reg.university,
                position=pos
            )

        messages.success(request, "Winners assigned successfully.")
        return redirect('assign-winners')


class StudentEventRegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = EventRegistrationForm()
        return render(request, 'students/students-events-register.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = EventRegistrationForm(request.POST, request.FILES)
        user = Users.objects.filter(profile=request.user).first()

        if not user:
            messages.error(request, "User profile not found. Please complete your profile before registering.")
            return redirect('students-view')

        if form.is_valid():
            event_title = form.cleaned_data['title']

            # 🔒 Prevent duplicate registration for the same event by the same student
            if ProfileDetails.objects.filter(student=user, title=event_title).exists():
                messages.error(request, "You have already registered for this event.")
                return redirect('send-request-fail')

            # Save the registration (but don't commit yet)
            registration = form.save(commit=False)
            registration.student = user

            # Calculate the age and set the category
            today = date.today()
            dob = registration.dob
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            if age <= 19:
                registration.category = "Junior"
            elif 20 <= age <= 22:
                registration.category = "Senior"
            else:
                registration.category = "Open"

            # Set the registration fee based on the category
            registration.registration_fee = registration_fees(registration.category)
            registration.created_at = timezone.now()
            registration.save()

            # Create the payment record
            Payment.objects.create(
                event=registration,
                amount=registration.registration_fee,
                student=registration.student
            )

            # Send the email notification
            subject = 'Your Event Registration Details'
            recipients = [registration.email]
            template = 'emails/registration-details.html'
            context = {
                'name': f'{registration.first_name} {registration.last_name}',
                'event': registration.title.title,
                'reg_number': registration.reg_number,
                'category': registration.category,
                'fee': registration.registration_fee,
                'institution': registration.institution,
            }

            send_email(subject, recipients, template, context)
            messages.success(request, "Registration successful! Details have been emailed to you.")
            
            # Print the UUID and redirect to Razorpay
            print("Redirecting to Razorpay with UUID:", registration.uuid)
            return redirect('razorpay', uuid=registration.uuid)

        # If form is not valid, render the registration page again
        return render(request, 'students/students-events-register.html', {"form": form})
