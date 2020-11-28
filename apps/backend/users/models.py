from django.db.models import constraints
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User

class Worker(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    rate_per_hour = models.DecimalField(max_digits=4, decimal_places=2)
    working = models.BooleanField(default=False)

class WorkTimestamp(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(default=now)
    working_after = models.BooleanField(default=True)
    location = models.CharField(max_length=40, default="Brak lokalizacji")

class AdditionalWorkTime(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date = models.DateField(default=now)
    time_minutes = models.IntegerField(default=0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'date'), name="user additional time work in day")
        ]