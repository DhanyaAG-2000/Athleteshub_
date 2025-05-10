
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm

from atheletes.models import Users   # Import Profile model
from django.contrib import messages
from django.conf import settings

import random

from django.utils import timezone

import threading
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

                # Ensure 'role' exists in the User model
                role = getattr(user, 'role', None)  # Safe way to access role

                if role == 'ADMIN':
                    return redirect('adminview')
                elif role in ['SPONSER']:
                    return redirect('sponsers-view')
                elif role == 'STUDENT':
                    return redirect('students-view')  # Ensure this URL name exists in urls.py

            # If authentication fails
            error = "Invalid username or password."

        else:
            error = "Invalid form submission."

        return render(request, 'authentication/login.html', {'form': form, 'error': error})

        
class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login')
    




    

    
  

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'password_reset/forgot-password.html')
    
    def post(self, request):
        email = request.POST.get('email')

        try:
            user = Users.objects.get(email=email, active_status=True)

            otp = random.randint(100000, 999999)

            request.session['reset_email'] = email
            request.session['reset_otp'] = otp
            request.session['otp_expiry'] = (timezone.now() + timedelta(minutes=5)).timestamp()

            subject = 'Password Reset OTP'
            context = {
                'name': f"{user.first_name} {user.last_name}",
                'otp': otp,
            }

            html_content = render_to_string('emails/password-reset-otp.html', context)
            plain_content = (
                f"Hi {user.first_name},\n\n"
                f"Your OTP for password reset is: {otp}\n"
                f"This OTP is valid for 5 minutes.\n\n"
                f"Regards,\nAthletesHub Team"
            )

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=plain_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            messages.success(request, 'An OTP has been sent to your email. Please check your inbox.')
            return redirect('verify-otp')

        except Users.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'password_reset/forgot-password.html')


class OTPVerificationView(View):
    def get(self, request):
        return render(request, 'password_reset/verify-otp.html')

    def post(self, request):
        entered_otp = request.POST.get('otp')
        reset_email = request.session.get('reset_email')
        session_otp = request.session.get('reset_otp')
        otp_expiry = request.session.get('otp_expiry')

        if not (reset_email and session_otp and otp_expiry):
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot-password')

        if timezone.now().timestamp() > otp_expiry:
            messages.error(request, 'OTP expired. Please request again.')
            return redirect('forgot-password')

        if int(entered_otp) == int(session_otp):
            return redirect('reset-password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'password_reset/verify-otp.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'password_reset/reset-password.html')

    def post(self, request):
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'password_reset/reset-password.html')

        reset_email = request.session.get('reset_email')

        if not reset_email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot-password')

        try:
            user = Users.objects.get(email=reset_email, active_status=True)
            profile = user.profile
            profile.set_password(password)
            profile.save()

            subject = 'Password Changed Successfully'
            context = {'name': user.first_name}

            html_content = render_to_string('emails/password-changed-confirmation.html', context)
            plain_content = (
                f"Hi {user.first_name},\n\n"
                f"Your password has been successfully changed.\n"
                f"If this wasn't you, please contact support immediately.\n\n"
                f"Regards,\nAthletesHub Team"
            )

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=plain_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[reset_email]
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            request.session.flush()

            messages.success(request, 'Password reset successfully! Please login.')
            return redirect('login')

        except Users.DoesNotExist:
            messages.error(request, 'Something went wrong. Please try again.')
            return redirect('forgot-password')

