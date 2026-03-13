from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Car, Favorite
from .forms import CarForm


def car_list(request):
    cars = Car.objects.all().order_by('-id')

    q = request.GET.get('q', '').strip()
    make = request.GET.get('make', '').strip()
    model = request.GET.get('model', '').strip()
    location = request.GET.get('location', '').strip()
    min_year = request.GET.get('min_year', '').strip()

    if q:
        cars = cars.filter(
            Q(title__icontains=q) |
            Q(make__icontains=q) |
            Q(model__icontains=q) |
            Q(location__icontains=q)
        )

    if make:
        cars = cars.filter(make__icontains=make)

    if model:
        cars = cars.filter(model__icontains=model)

    if location:
        cars = cars.filter(location__icontains=location)

    if min_year:
        try:
            cars = cars.filter(year__gte=int(min_year))
        except:
            pass

    return render(request, 'cars/car_list.html', {'cars': cars})


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, car=car).exists()

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'is_favorited': is_favorited
    })


@login_required
def post_car(request):

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)

        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()

            return redirect('car_detail', car_id=car.id)

    else:
        form = CarForm()

    return render(request, 'cars/post_car.html', {'form': form})


@login_required
def my_cars(request):

    cars = Car.objects.filter(owner=request.user)

    return render(request, 'cars/my_cars.html', {
        'cars': cars
    })


@login_required
def edit_car(request, car_id):

    car = get_object_or_404(Car, id=car_id, owner=request.user)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)

        if form.is_valid():
            form.save()
            return redirect('my_cars')

    else:
        form = CarForm(instance=car)

    return render(request, 'cars/edit_car.html', {
        'form': form
    })


@login_required
def delete_car(request, car_id):

    car = get_object_or_404(Car, id=car_id, owner=request.user)

    car.delete()

    return redirect('my_cars')


@login_required
def toggle_favorite(request, car_id):

    car = get_object_or_404(Car, id=car_id)

    favorite = Favorite.objects.filter(user=request.user, car=car)

    if favorite.exists():
        favorite.delete()
    else:
        Favorite.objects.create(user=request.user, car=car)

    return redirect('car_detail', car_id=car.id)


@login_required
def saved_cars(request):

    favorites = Favorite.objects.filter(user=request.user)\
        .select_related('car')\
        .order_by('-created_at')

    return render(request, 'cars/saved_cars.html', {
        'favorites': favorites
    })


def autocomplete_ads(request):

    term = request.GET.get('term', '').strip()

    suggestions = []

    if term:
        makes = list(Car.objects.filter(make__icontains=term)
                     .values_list('make', flat=True)
                     .distinct())

        models = list(Car.objects.filter(model__icontains=term)
                      .values_list('model', flat=True)
                      .distinct())

        titles = list(Car.objects.filter(title__icontains=term)
                      .values_list('title', flat=True)
                      .distinct())

        locations = list(Car.objects.filter(location__icontains=term)
                         .values_list('location', flat=True)
                         .distinct())

        for item in makes + models + titles + locations:
            if item and item not in suggestions:
                suggestions.append(item)

    return JsonResponse({
        'suggestions': suggestions[:8]
    })


def get_models(request):

    make = request.GET.get('make')

    models = Car.objects.filter(make__iexact=make)\
        .values_list('model', flat=True)\
        .distinct()

    return JsonResponse({
        'models': list(models)
    })
def configurator(request):
    makes = Car.objects.values_list('make', flat=True).distinct().order_by('make')
    return render(request, 'cars/configurator.html', {
        'makes': makes
    })