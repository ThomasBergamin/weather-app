from django.urls import path
from . import views
from .views import CityDeleteView

urlpatterns = [
    path('', views.get_weather, name='home'),
    path('city/<city_name>/', views.get_city_details, name='city_detail'),
    path('city/delete/<int:pk>', CityDeleteView.as_view(), name='delete_city'),
]
