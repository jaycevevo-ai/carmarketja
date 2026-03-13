from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from cars.models import Car


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                is_dealer=False
            )
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def dealer_store(request, username):
    dealer_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=dealer_user)
    cars = Car.objects.filter(owner=dealer_user).order_by('-id')

    return render(request, 'users/dealer_store.html', {
        'profile': profile,
        'dealer_user': dealer_user,
        'cars': cars,
        'car_count': cars.count(),
    })


@login_required
def dealer_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)

    if not profile.is_dealer:
        return redirect('home')

    cars = Car.objects.filter(owner=request.user).order_by('-id')

    return render(request, 'users/dealer_dashboard.html', {
        'profile': profile,
        'cars': cars,
        'car_count': cars.count(),
    })