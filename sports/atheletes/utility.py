import uuid
import string
import random
from .models import Users
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def get_registration_number():
    """Generate a unique registration number."""
    while True:
        pattern = str(uuid.uuid4().int)[:7]
        reg_number = f'SM-{pattern}'
        if not Users.objects.filter(reg_number=reg_number).exists():
            return reg_number

def get_password():
    """Generate a random 8-character password."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def send_email(subject, recipients, template, context):
    """Send an HTML email."""
    try:
        content = render_to_string(template, context)
        email_obj = EmailMultiAlternatives(
            subject=subject,
            body=content,
            from_email=settings.EMAIL_HOST_USER,
            to=recipients
        )
        email_obj.attach_alternative(content, 'text/html')
        email_obj.send()
    except Exception as e:
        print(f"Email sending failed: {e}")  # Debugging purpose

