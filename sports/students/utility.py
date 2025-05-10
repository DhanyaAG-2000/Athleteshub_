


from django.shortcuts import render, get_object_or_404
from .models import Users
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags  # Ensure you import this

def send_email(subject, recipients, template, context):
    """Send an HTML email with plain text and HTML versions."""
    try:
        # Render HTML content from the template and context
        html_content = render_to_string(template, context)
        plain_content = strip_tags(html_content)  # Convert HTML to plain text

        # Log the email content for debugging
        print(f"Sending email to: {recipients}")
        print(f"Subject: {subject}")
        print(f"HTML Content: {html_content}")
        print(f"Plain Content: {plain_content}")

        # Create an email object with both plain text and HTML parts
        email_obj = EmailMultiAlternatives(
            subject=subject,
            body=plain_content,  # Plain-text version
            from_email=settings.EMAIL_HOST_USER,  # From email
            to=recipients,  # To email
        )

        # Attach the HTML content as an alternative
        email_obj.attach_alternative(html_content, 'text/html')

        # Send the email
        email_obj.send()
        print("Email sent successfully.")

    except Exception as e:
        print(f"Email sending failed: {e}")  # Debugging purpose




def registration_fees(category):
    if category == "Junior":
        return "150"
    elif category == "Senior":
        return "200"
    else:
        return "250"