

r
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_email(subject, recipients, template, context):
    """
    Send an HTML email with a plain text fallback.
    """
    try:
        # Render the HTML content from template
        html_content = render_to_string(template, context)

        # Plain text fallback
        text_content = f"{context.get('name', 'User')}, your OTP is {context.get('otp', '')}."

        

        # Create and send the email
        email_obj = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=recipients
        )
        email_obj.attach_alternative(html_content, 'text/html')
        email_obj.send()

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")
