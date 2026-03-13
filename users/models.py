from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_dealer = models.BooleanField(default=False)
    dealer_name = models.CharField(max_length=200, blank=True, null=True)
    dealer_logo = models.ImageField(upload_to='dealer_logos/', blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def _str_(self):
        return self.user.username