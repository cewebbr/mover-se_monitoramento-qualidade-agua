from django.db import models
from django.contrib.auth.models import User


class WaterSource(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    identification = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    latitude = models.DecimalField(
        max_digits=25, decimal_places=20, default=None)
    longitude = models.DecimalField(
        max_digits=25, decimal_places=20, default=None)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ("-datetime_creation",)
