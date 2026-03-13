from django.shortcuts import render
from cars.models import Car


def home(request):
    latest_cars = Car.objects.all().order_by('-id')[:8]
    cheap_cars = Car.objects.filter(price__lte=1000000).order_by('-id')[:8]
    pickups = Car.objects.filter(
        model__icontains='hilux'
    ).order_by('-id')[:8]

    total_ads = Car.objects.count()

    return render(request, 'home.html', {
        'latest_cars': latest_cars,
        'cheap_cars': cheap_cars,
        'pickups': pickups,
        'total_ads': total_ads,
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')