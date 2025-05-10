from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View

from .forms import UsersRegisterForm

from django.db import transaction

from .utility import get_registration_number,get_password,send_email

from authentication.models import Profile

from django.utils.timezone import now

from django.db.models import Q

from .models import Users






# Create your views here.

class DashboardView(View):

    def get(self,request,*args,**kwargs):

        user_details = Users.objects.filter(profile=request.user).first()

        return render(request,'Dashboard/dashboard.html',{"user_details":user_details})
    

    
class ContactView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'Dashboard/contact.html') 


class  AdminView(View):

    def get(self,request,*args,**kwargs):

        user_details = Users.objects.filter(profile=request.user).first()

        return render(request,'admin/admin-view.html',{'user_details': user_details})
  
        
class UserListView(View):
     
     def get(self,request,*args,**kwargs): 


        users = Users.objects.filter(active_status = True)

       

        return render(request,"admin/user-management.html",{'users' :users}) #,context=data
   

class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = UsersRegisterForm()
        return render(request, 'atheletes/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UsersRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            
            with transaction.atomic():

                user = form.save(commit=False)

                user.reg_number = get_registration_number()
               
                username = user.email
                password = get_password()
                role = user.rolechoice

                print("The role is:", role)

                # Set last login to current time
                user.last_login = now()

                # Create user profile
                profile = Profile.objects.create_user(username=username, password=password, role=role)
                user.profile = profile

                user.save()

                # Sending login credentials via email
                subject = 'Your Password for Sports Management'
                recipients = [user.email]
                template = 'emails/login-credential.html'  # Ensure this file exists

                context = {
                    "reg_number": user.reg_number,
                    'name': f'{user.first_name} {user.last_name}',
                    "username": username,
                    "password": password,
                    "role": role
                }

                try:
                    send_email(subject, recipients, template, context)
                except Exception as e:
                    print(f"Error sending email: {e}")  # Debugging purpose

                return redirect('dashboard')

        return render(request, "atheletes/registration.html", {'form': form})

class GetUserObject:


    def get_user(self,request,uuid):

        try :

            user = Users.objects.get(uuid=uuid)

            return user
        
        except :

            return render(request,"error/error-404.html")
        
class UserDetailView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')
        
        user = get_object_or_404(Users, uuid=uuid)

        data ={'user':user}

        return render(request,'atheletes/detail-view.html',context=data)

 
    
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Users
from .forms import UsersRegisterForm

class UserUpdateView(View):
    
    def get(self, request, *args, **kwargs):
        # Get the logged-in user
        user = get_object_or_404(Users, profile=request.user)

        # Instantiate the form with the user's data
        form = UsersRegisterForm(instance=user)
        
        # Return the form to the template
        return render(request, 'atheletes/user-update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        # Get the logged-in user
        user = get_object_or_404(Users, profile=request.user)
        
        # Bind the form with POST data and the user instance
        form = UsersRegisterForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Save the form data
            form.save()
            return redirect('send-request-success')
        
        # If the form is not valid, re-render with the form and errors
        return render(request, 'atheletes/user-update.html', {'form': form})

        

class SuccessfullyregisteredView(View):

     def get(self,request,*args,**kwargs):

        return render(request,'successnote.html')
        

class EventCompainingView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'compaining.html')

from django.core.mail import send_mail
from django.conf import settings




from django.views import View
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

class UserDeleteView(View):

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')

        # Get the user object (to be deactivated)
        user = GetUserObject().get_user(request, uuid)

        # Deactivate the user
        user.active_status = False
        user.save()

        # Safely get admin's email address
        admin_email = (
            request.user.email or
            getattr(getattr(request.user, 'profile', None), 'email', None) or
            getattr(getattr(request.user, 'users', None), 'email', None) or
            'support@athleteshub.com'
        )

        # Email subject and recipient
        subject = "Account Deactivation Notice"
        recipient_list = [user.email]

        # Render HTML email template
        html_message = render_to_string('emails/account_deactivation_email.html', {
            'user': user,
            'admin_email': admin_email,
        })

        # Plain text version of the message
        plain_message = (
            f"Dear {user.first_name} {user.last_name},\n\n"
            f"We regret to inform you that your account on AthletesHub has been deactivated by the administrator."
            f"\nIf you believe this is a mistake or have any concerns, please contact {admin_email}."
            f"\n\nBest regards,\nAthletesHub Team"
        )

        # Create and send the email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
            reply_to=[admin_email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

        return redirect('user-management')
