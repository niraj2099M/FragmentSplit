from django.db import models
from django.core.validators import MinValueValidator

from django.utils import timezone

class players(models.Model):
    name = models.CharField(max_length=255,unique=True)
    fragNo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    wz = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}: Frags- {self.fragNo}, Wz(mill)- {self.wz}"


class sess(models.Model):

    dateSession=models.DateField()
    time_of_day = models.CharField(max_length=7, choices=[('morning', 'Morning'), ('night', 'Night')])
    noFrag = models.PositiveIntegerField()
    wzCollected = models.PositiveIntegerField()
    noPlayers=models.PositiveIntegerField()
    player_ids=models.CharField(max_length=255, default="1,2,3")


    def __str__(self):
        return f"{self.dateSession}: Frags- {self.noFrag}, Wz(million)- {self.wzCollected}, No. of players- {self.noPlayers}"
    


class payoutData(models.Model):
    name = models.CharField(max_length=255)
    current_datetime_ist = models.DateTimeField(default=timezone.now)
    fragsPaid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    wzPaid = models.IntegerField(default=0, validators=[MinValueValidator(0)])
  

    def __str__(self):
        return f"{self.name} got paid {self.fragsPaid} Frags & {self.wzPaid} wz @ {self.current_datetime_ist}"