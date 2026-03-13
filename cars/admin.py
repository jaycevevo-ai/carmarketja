from django.contrib import admin
from .models import Car, CarImage, Favorite


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 14


class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]


admin.site.register(Car, CarAdmin)
admin.site.register(Favorite)