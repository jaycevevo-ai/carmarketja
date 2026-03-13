from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.IntegerField()
    transmission = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.title = f"{self.year} {self.make} {self.model} – {self.mileage:,} km – {self.transmission}"
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.year}-{self.make}-{self.model}-{self.id}")
            super().save(update_fields=["slug"])

    def _str_(self):
        return self.title


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='car_gallery/')

    def _str_(self):
        return f"Photo for {self.car.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def _str_(self):
        return f"{self.user.username} saved {self.car.title}"