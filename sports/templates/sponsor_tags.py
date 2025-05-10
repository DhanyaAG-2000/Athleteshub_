# sponsers/templatetags/sponsor_tags.py

from django import template
from sponsers.models import Users

register = template.Library()

@register.filter
def get_request_for_user(requests, user):
    try:
        student = Users.objects.get(profile=user)
        return requests.filter(student=student).first()
    except Users.DoesNotExist:
        return None
