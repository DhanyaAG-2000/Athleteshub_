from django.db import models


class SPORT_CHOICES(models.TextChoices) : 
        
      FOOTBALL=  'football', 'Football'

      CRICKET='cricket', 'Cricket'

      BASKETBALL='basketball', 'Basketball'

      VOLLEYBALL='volleyball', 'Volleyball'

      BADMINTON='badminton', 'Badminton'

      TENNIS='tennis', 'Tennis'

      HOCKEY='hockey', 'Hockey'



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


class SportsEvent(models.Model): 



    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES.choices)

    title = models.CharField(max_length=200)

    description = models.TextField()

    image = models.ImageField(upload_to='sports_events')

    date = models.DateField(null=True, blank=True)

    time = models.TimeField(null=True, blank=True)

    venue = models.CharField(max_length=255)

    district = models.CharField(max_length=20,choices=DistrictChoices.choices)


    reg_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title}"
