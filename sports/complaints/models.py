from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('suggestion', 'Suggestion'),
        ('complaint', 'Complaint'),
        ('praise', 'Praise'),
        ('other', 'Other'),
    ]

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 stars

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.ForeignKey('atheletes.Users',null=True,on_delete=models.SET_NULL) 
    subjects = models.CharField(max_length=100) # Updated from issues to subject
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    message = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    usefulness_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)  # How helpful the feedback is
    submitted_at = models.DateTimeField(auto_now_add=True)
    screenshot = models.ImageField(upload_to='feedback_screenshots/', null=True, blank=True)

    def __str__(self):
        return f"Feedback on {self.subject} by {self.user.username}"
