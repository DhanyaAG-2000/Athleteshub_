from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from atheletes.models import Users
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator






def send_password_reset_email(user):
    """Generate token and send password reset email."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.SITE_URL}/authentication/password-reset/{uid}/{token}/"

    subject = "Password Reset Request"
    message = render_to_string("password_reset/password_reset_email.html", {"reset_link": reset_link})  # ✅ Correct path

    send_mail(subject, "", settings.EMAIL_HOST_USER, [user.email], html_message=message)

def validate_reset_token(uidb64, token):
    """Validate password reset token and return user if valid."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            return user
    except (Users.DoesNotExist, ValueError, TypeError):
        return None

def send_password_reset_email(user):
    """
    Generates a password reset token and sends an email to the user.
    """

    # ✅ Dynamically add missing methods/attributes
    if not hasattr(user, "get_email_field_name"):
        user.get_email_field_name = lambda: "email"

    if not hasattr(user, "password"):  
        user.password = "temporarypassword"  # Fake password to satisfy token generator

    # Generate token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Construct reset link
    site_url = getattr(settings, "SITE_URL", "http://localhost:8000")  # Fallback to local URL
    reset_link = f"{site_url}/authentication/password-reset-confirm/{uid}/{token}/"

    # Send email
    subject = "Password Reset Request"
    message = f"Click the link below to reset your password:\n{reset_link}"
    user.email_user(subject, message)




def send_password_reset_email(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # Generate the reset link dynamically
    reset_link = f"{settings.SITE_URL}{reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})}"
    
    subject = "Password Reset Request"
    message = f"Click the link below to reset your password:\n{reset_link}\nIf you didn't request this, ignore this email."

    # Ensure user model has 'email_user' or use send_mail
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])




def send_password_reset_email(user):
    """Generate token and send a password reset email."""
    
    # Override get_email_field_name dynamically
    if not hasattr(user, "get_email_field_name"):
        user.get_email_field_name = lambda: "email"

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    reset_link = f"{settings.SITE_URL}/authentication/password-reset-confirm/{uid}/{token}/"
    
    subject = "Reset Your Password"
    message = f"Click the link to reset your password: {reset_link}"
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def generate_password_reset_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # React frontend base URL
    react_base_url = "http://your-react-app.com/reset-password"
    
    # Full reset link to be sent via email
    reset_link = f"{react_base_url}/{uid}/{token}"
    return reset_link
