from .models import SportsEvent
import uuid
def get_registration_number():
    """Generate a unique registration number."""
    while True:
        pattern = str(uuid.uuid4().int)[:5]
        reg_number = f'SE-{pattern}'
        if not SportsEvent.objects.filter(reg_number=reg_number).exists():
            return reg_number