from django.urls import path
from .views import register, dealer_store, dealer_dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dealer/<str:username>/', dealer_store, name='dealer_store'),
    path('dealer-dashboard/', dealer_dashboard, name='dealer_dashboard'),
]