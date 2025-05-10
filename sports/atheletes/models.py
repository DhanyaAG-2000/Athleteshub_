
from django.db import models
import uuid
from authentication.models import Rolechoice

# Create your models here.

class BaseClass(models.Model):
   
   uuid = models.SlugField(unique=True,default=uuid.uuid4)

   active_status = models.BooleanField(default=True)

   created_at = models.DateTimeField(auto_now_add=True)

   updated_at = models.DateTimeField(auto_now=True)

   class Meta :
      
      abstract = True



class DistrictChoices(models.TextChoices):

   THIRUVANANTHAPURAM = 'THIRUVANANTHAPURAM','THIRUVANANTHAPURAM'
   KOLLAM = 'KOLLAM','KOLLAM'
   PATHANAMTHITTA = 'PATHANAMTHITTA','PATHANAMTHITTA'
   ALAPPUZHA = 'ALAPPUZHA','ALAPPUZHA'
   KOTTAYAM = 'KOTTAYAM','KOTTAYAM'
   IDUKKI = 'IDUKKI','IDUKKI'
   ERNAKULAM = 'ERNAKULAM','ERNAKULAM'
   THRISSUR = 'THRISSUR','THRISSUR'
   PALAKKAD = 'PALAKKAD','PALAKKAD'
   MALAPPURAM = 'MALAPPURAM','MALAPPURAM'
   KOZHIKODE = 'KOZHIKODE','KOZHIKODE'
   WAYANAD = 'WAYANAD','WAYANAD'
   KANNUR = 'KANNUR','KANNUR'
   KASARGOD = 'KASARGOD','KASARGOD'




class Users(BaseClass):

#personal details

    profile=models.OneToOneField('authentication.profile',on_delete=models.CASCADE)

    rolechoice = models.CharField(max_length=20,choices=Rolechoice.choices)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    photo = models.ImageField(upload_to='Users')

    email = models.EmailField(unique=True)

    contact_num = models.CharField(max_length=20)

    house_name = models.CharField(max_length=40)

    post_office = models.CharField(max_length=50)

    district = models.CharField(max_length=20,choices=DistrictChoices.choices)

    pincode = models.CharField(max_length=10)

    join_date=models.DateTimeField(auto_now=True)

   #   registration Number

    reg_number = models.CharField(max_length=20)

   
    # Add last_login to fix password reset issue
    last_login = models.DateTimeField(blank=True, null=True) 

   #  user type


    def __str__(self):

     return f'{self.first_name} {self.last_name} '
    
    class Meta :
       
       verbose_name = 'users'
       verbose_name_plural = 'users'

       ordering = ['-id']

    
    