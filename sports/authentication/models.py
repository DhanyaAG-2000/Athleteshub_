from django.db import models

from django.contrib.auth.models import User

from django.contrib.auth.models import  AbstractUser

# Create your models here.

class Rolechoice(models.TextChoices):

    ADMIN='ADMIN','ADMIN'

    STUDENT='STUDENT','STUDENT'

    SPONSER='SPONSER','SPONSER'

class Profile(AbstractUser):
    

    role=models.CharField(max_length=30,choices=Rolechoice.choices)

    def __str__(self):

        print(self.role)

        return f'{self.username}-{self.role}'
    

    
    class Meta:

        verbose_name='profile'

        verbose_name_plural='profile'