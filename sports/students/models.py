# from django.db import models
# from atheletes.models import DistrictChoices, Users
# from events.models import SportsEvent
# from django.utils import timezone


# class Gender(models.TextChoices):
#     Male = 'Male', 'Male'
#     Female = 'Female', 'Female'
#     Others = 'Others', 'Others'

# class ProfileDetails(models.Model):
    
#     title = models.ForeignKey("events.SportsEvent", on_delete=models.CASCADE)  # Connect to the SportsEvent model
#     reg_number = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     dob = models.DateField()
#     gender = models.CharField(max_length=20, choices=Gender.choices)
#     email = models.EmailField()
#     address = models.CharField(max_length=150)
#     student_district = models.CharField(max_length=100, choices=DistrictChoices.choices)
#     pincode = models.CharField(max_length=10)
#     phone = models.CharField(max_length=15)
#     institution = models.CharField(max_length=100)
#     institution_districts = models.CharField(max_length=100, choices=DistrictChoices.choices)
#     university = models.CharField(max_length=100)
#     Id_proof = models.FileField(upload_to='images', blank=True, null=True)
#     registration_fee = models.CharField(max_length=5)
#     category = models.CharField(max_length=50, blank=True, null=True)  # Category should be auto-calculated later
#     created_at = models.DateTimeField(default=timezone.now)
#     student = models.ForeignKey('atheletes.Users',null=True,on_delete=models.SET_NULL)


#     def __str__(self):
#         return f"{self.first_name} {self.last_name} - {self.reg_number}"

#     class Meta:
#         verbose_name = 'Profile Details'
#         verbose_name_plural = 'Profile Details'
#         ordering = ['-created_at']



# # models.py
# from django.db import models
# from events.models import SportsEvent  # Assuming SportsEvent model is in the events app
# from atheletes.models import Users  # Assuming Users model is in the atheletes app

# class EventWinner(models.Model):
#     POSITION_CHOICES = [
#         ('1st', '1st'),
#         ('2nd', '2nd'),
#         ('3rd', '3rd'),
#     ]
    
#     CATEGORY_CHOICES = [
#         ('Junior', 'Junior'),
#         ('Senior', 'Senior'),
#         ('Open', 'Open'),
#     ]
    
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     registered_event = models.ForeignKey(SportsEvent, on_delete=models.CASCADE)  # Event the student participated in
#     institution = models.CharField(max_length=100)
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Dropdown for category
#     university = models.CharField(max_length=100)
#     position = models.CharField(max_length=10, choices=POSITION_CHOICES)  # 1st, 2nd, or 3rd place

#     class Meta:
#         verbose_name = 'Event Winner'
#         verbose_name_plural = 'Event Winners'
#         unique_together = ['registered_event', 'position']  # Ensure only one winner per position per event

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} - {self.registered_event.title} ({self.position})"
   


 































from django.db import models
from atheletes.models import DistrictChoices, Users
from events.models import SportsEvent
from django.utils import timezone

from atheletes. models import BaseClass


class Gender(models.TextChoices):
    Male = 'Male', 'Male'
    Female = 'Female', 'Female'
    Others = 'Others', 'Others'

class ProfileDetails(BaseClass):
    
    title = models.ForeignKey("events.SportsEvent", on_delete=models.CASCADE)  # Connect to the SportsEvent model
    reg_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=Gender.choices)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    student_district = models.CharField(max_length=100, choices=DistrictChoices.choices)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    institution = models.CharField(max_length=100)
    institution_districts = models.CharField(max_length=100, choices=DistrictChoices.choices)
    university = models.CharField(max_length=100)
    Id_proof = models.FileField(upload_to='images', blank=True, null=True)
    registration_fee = models.CharField(max_length=5)
    category = models.CharField(max_length=50, blank=True, null=True)  # Category should be auto-calculated later
    
    student = models.ForeignKey('atheletes.Users',null=True,on_delete=models.SET_NULL)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reg_number}"

    class Meta:
        verbose_name = 'Profile Details'
        verbose_name_plural = 'Profile Details'
        ordering = ['-created_at']



# models.py
from django.db import models
from events.models import SportsEvent  # Assuming SportsEvent model is in the events app
from atheletes.models import Users  # Assuming Users model is in the atheletes app

class EventWinner(models.Model):
    POSITION_CHOICES = [
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
    ]
    
    CATEGORY_CHOICES = [
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
        ('Open', 'Open'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    registered_event = models.ForeignKey(SportsEvent, on_delete=models.CASCADE)  # Event the student participated in
    institution = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Dropdown for category
    university = models.CharField(max_length=100)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)  # 1st, 2nd, or 3rd place

    class Meta:
        verbose_name = 'Event Winner'
        verbose_name_plural = 'Event Winners'
        unique_together = ['registered_event', 'position']  # Ensure only one winner per position per event

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.registered_event.title} ({self.position})"
   