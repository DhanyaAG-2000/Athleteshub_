from decouple import config
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm

from atheletes.models import Users   # Import Profile model
from django.contrib import messages
from django.conf import settings
from authentication.utility import send_password_reset_email, validate_reset_token

from django.core.mail import send_mail
from .utility import generate_password_reset_link
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
    template_name = "password_reset/password_reset.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = Users.objects.get(email=email)

            # ✅ Ensure last_login exists
            if not hasattr(user, "last_login"):
                user.last_login = None  

            # ✅ Ensure password exists
            if not hasattr(user, "password"):  
                user.password = ""  # Set a default empty password if missing

            send_password_reset_email(user)
            messages.success(request, "Password reset link has been sent to your email.")
        except Users.DoesNotExist:
            messages.error(request, "No account found with this email.")

        return redirect("password_reset")  # ✅ Fixed redirect

class ConfirmPasswordResetView(View):
    template_name = "password_reset/password_reset_confirm.html"

    def get(self, request, uidb64, token):
        user = validate_reset_token(uidb64, token)
        if user:
            return render(request, self.template_name, {"uidb64": uidb64, "token": token})
        messages.error(request, "Invalid or expired reset link.")
        return redirect("password_reset")  #  Fixed redirect

    def post(self, request, uidb64, token):
        password = request.POST.get("password")
        user = validate_reset_token(uidb64, token)
        if user:
            user.set_password(password)
            user.save()
            messages.success(request, "Your password has been updated successfully.")
            return redirect("login")  #  Fixed redirect

        messages.error(request, "Invalid or expired reset link.")
        return redirect("password_reset")



def send_password_reset_email(request, user):
    user=Users.objects.get('email')
    reset_link = generate_password_reset_link(user)
    message = render_to_string('reset_password_email.html', {
    'reset_link': reset_link
    })

    send_mail(
        subject="Reset Your Password",
        message="Please view this email in HTML format.",
        from_email=config('EMAIL_HOST_USER'),
        recipient_list=[user.email],
        html_message=message
         )

      


    

    


    
