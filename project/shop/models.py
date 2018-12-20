from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    manager = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start = models.TimeField()
    end = models.TimeField()
    region = models.CharField(max_length=200, blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    notice = models.TextField(blank=True, null=True)
    appid = models.CharField(max_length=200, blank=True, null=True)
    secret = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
