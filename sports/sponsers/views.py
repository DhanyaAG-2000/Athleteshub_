

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SponsorCompany
from atheletes.models import Users
from students.models import ProfileDetails
from .forms import SponsorCompanyForm
from .models import  SponsorCompany,SponsorshipRequest
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse


   
# 1
class SponsersView(View):

    def get(self, request, *args, **kwargs):

        user_details = Users.objects.filter(profile=request.user).first()
        
        return render(request,'sponsers/sponsers-view.html',{'user_details': user_details})

#2
class SponsorsListView(View):

    def get(self, request, *args, **kwargs):
        
        sponsors = SponsorCompany.objects.all()
        
        return render(request, 'sponsers/sponsers-list.html', {"sponsors": sponsors})




#3
class SponsorAthleteListView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        users = ProfileDetails.objects.all()

        if search_query:
            users = users.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(institution__icontains=search_query) |
                Q(university__icontains=search_query)|
                Q(first_name__icontains=search_query) & Q(last_name__icontains=search_query)
 
               
            )

        return render(request, 'sponsers/view_athletes.html', {
            'users': users,
            'search_query': search_query
        })

# #4   


class SponsorCompanyView(View):

    def get(self, request, *args, **kwargs):
        try:
            sponsor = Users.objects.get(profile=request.user)

            # Check if this sponsor already has a company
            if SponsorCompany.objects.filter(sponsor=sponsor).exists():
                 return redirect('send-request-fail')

            form = SponsorCompanyForm()
            return render(request, 'sponsers/sponsor-company.html', {'form': form})

        except Users.DoesNotExist:
            return HttpResponse('Sponsor user not found.', status=403)

    def post(self, request, *args, **kwargs):
        try:
            sponsor = Users.objects.get(profile=request.user)

            # Prevent duplicate registration
            if SponsorCompany.objects.filter(sponsor=sponsor).exists():
                return redirect('send-request-fail')

            form = SponsorCompanyForm(request.POST, request.FILES)
            if form.is_valid():
                registration = form.save(commit=False)
                registration.sponsor = sponsor
                registration.save()
                return redirect('success')

        except Users.DoesNotExist:
            return HttpResponse('Sponsor user not found.', status=403)

        return render(request, 'sponsers/sponsor-company.html', {'form': form})
  
class RequestsendsuccessfullyView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'sendrequest.html')
    
  
class RequestsendFailView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'failrequest.html')    


class StudentRequestCompanyView(View):

     def get(self, request, *args, **kwargs):
         
         sponsors = SponsorCompany.objects.all()
         
         return render(request, 'requests/student-sponsor-request.html', {'sponsors': sponsors})
     

@method_decorator(login_required, name='dispatch')
class SendSponsorshipRequestView(View):
    
    def post(self, request, sponsor_id):
        student = Users.objects.get(profile=request.user)
        sponsor = get_object_or_404(SponsorCompany, id=sponsor_id)

        # Prevent duplicate requests
        already_sent = SponsorshipRequest.objects.filter(student=student, sponsor=sponsor).exists()

        if already_sent:
            return redirect('send-request-fail')  # request already exists

        # Create the request if not already sent
        SponsorshipRequest.objects.create(student=student, sponsor=sponsor, status='pending')

        
        return redirect('send-request-success')
    

@method_decorator(login_required, name='dispatch')
class SponsorRequestManageView(View):
    def get(self, request):
        try:
            user_instance = Users.objects.get(profile=request.user)
            print(f"User instance: {user_instance}")
        except Users.DoesNotExist:
            print("User instance not found.")
            return render(request, 'requests/request-sponser.html', {'combined_data': []})

        try:
            sponsor = SponsorCompany.objects.get(sponsor=user_instance)
            print(f"Sponsor company: {sponsor}")
        except SponsorCompany.DoesNotExist:
            print("Sponsor company not found.")
            return render(request, 'requests/request-sponser.html', {'combined_data': []})

        requests = SponsorshipRequest.objects.filter(sponsor=sponsor).select_related('student')
        print(f"Found {requests.count()} sponsorship requests.")

        combined_data = []
        for req in requests:
            try:
                profile = ProfileDetails.objects.filter(student=req.student).first()
                if profile:
                    combined_data.append({
                        'first_name': profile.first_name,
                        'last_name': profile.last_name,
                        'email': req.student.email,
                        'phone': profile.phone,
                        'university': profile.university,
                        'institution': profile.institution,
                        'message': req.message,
                        'status': req.status,
                        'created_at': req.created_at,
                        'id': req.id,
                    })
            except ProfileDetails.DoesNotExist:
                continue

        print(f"Combined data: {combined_data}")
        return render(request, 'requests/request-sponser.html', {'combined_data': combined_data})






@method_decorator(login_required, name='dispatch')
class AdminSponsorshipOverviewView(View):
    def get(self, request, *args, **kwargs):
        all_requests = SponsorshipRequest.objects.select_related('student', 'sponsor__sponsor').all()
        return render(request, 'requests/admin-pending-requests.html', {'requests': all_requests})
    
 
class queryView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'query.html')    
  
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class ChangeRequestStatusView(View):
    def post(self, request, request_id):
        req = get_object_or_404(SponsorshipRequest, id=request_id)
        message = request.POST.get('response_message', '')

        # Determine action based on URL name
        url_name = request.resolver_match.url_name
        if url_name == 'accept-request':
            req.status = 'Accepted'
        elif url_name == 'reject-request':
            req.status = 'Rejected'
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        req.response_message = message
        req.responded_at = timezone.now()
        req.save()

        # Send email to the student
        profile = req.student
        if profile and profile.email:
            subject = f"Sponsorship Request {req.status}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [profile.email]

            context = {
                'student_name': profile.first_name,
                'status': req.status,
                'sponsor_message': req.response_message,
                'sponsor_name': req.sponsor.company_name,
            }

            text_body = render_to_string('emails/sponsorship_status.txt', context)
            html_body = render_to_string('emails/sponsorship_status.html', context)

            msg = EmailMultiAlternatives(subject, text_body, from_email, to_email)
            msg.attach_alternative(html_body, "text/html")
            msg.send()

        return redirect('query')
















