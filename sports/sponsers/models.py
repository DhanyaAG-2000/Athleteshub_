# models.py

from django.db import models
from django.utils import timezone




class STATUS_CHOICES(models.TextChoices):
        
        pending='pending', 'Pending'
        accepted='accepted', 'Accepted'
        rejected='rejected', 'Rejected'
    
class SponsorCompany(models.Model):
    
    sponsor = models.ForeignKey('atheletes.Users',null=True,on_delete=models.SET_NULL)
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField()
    company_phone = models.CharField(max_length=20, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    location=models.CharField(max_length=200,blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='sponsor_logos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sponsor} -{self.company_name} "



class SponsorshipRequest(models.Model):
    

    student = models.ForeignKey('atheletes.Users', on_delete=models.CASCADE)
    sponsor = models.ForeignKey(SponsorCompany, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    response_message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} -> {self.sponsor} [{self.status}]"



















































