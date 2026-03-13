from django.urls import path
from .views import (
    car_list,
    car_detail,
    post_car,
    my_cars,
    saved_cars,
    toggle_favorite,
    edit_car,
    delete_car,
    autocomplete_ads,
    get_models,
    configurator,
)

urlpatterns = [
    path('', car_list, name='car_list'),
    path('configurator/', configurator, name='configurator'),
    path('post/', post_car, name='post_car'),
    path('my-cars/', my_cars, name='my_cars'),
    path('saved/', saved_cars, name='saved_cars'),
    path('favorite/<int:car_id>/', toggle_favorite, name='toggle_favorite'),
    path('edit/<int:car_id>/', edit_car, name='edit_car'),
    path('delete/<int:car_id>/', delete_car, name='delete_car'),
    path('autocomplete/', autocomplete_ads, name='autocomplete_ads'),
    path('get-models/', get_models, name='get_models'),
    path('car/<int:car_id>/', car_detail, name='car_detail'),
]