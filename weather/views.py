from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from .forms import CityForm

from .models import City
import os
import environ

import requests

# Read env file
env = environ.Env()
environ.Env.read_env()

# Create your views here.

weather_url = 'https://api.openweathermap.org/data/2.5/weather'
weather_api_key = env('WEATHER_KEY')


def get_weather(request):

    error_message = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():

            new_city = form.cleaned_data['name']

            # prevent duplicates
            existing_city_number = City.objects.filter(name=new_city).count()

            if existing_city_number == 0:
                # check if city was found in the API
                weather_parameters = {
                    'q': new_city,
                    'appid': weather_api_key,
                    'units': 'metric'
                }
                response = requests.get(weather_url, params=weather_parameters).json()
                if response['cod'] != 200:
                    error_message = 'City does not exist'
                else:
                    form.save()
            else:
                error_message = 'There is already a city with this name.'
        if error_message:
            message = error_message
            message_class = 'danger'
        else:
            message = 'City added successfully!'
            message_class = 'success'

    # always display the form :
    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:
        weather_parameters = {
            'q': city.name,
            'appid': weather_api_key,
            'units': 'metric'
        }
        response = requests.get(weather_url, params=weather_parameters)
        data = response.json()
        city_weather = {
            'city': city.name,
            'country': data['sys']['country'],
            'temp': round(data['main']['temp'], 1),
            'humidity': data['main']['humidity'],
            'pk': city.pk,
            'icon': data['weather'][0]['icon'],
            'description': data['weather'][0]['description'].title(),
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
    }
    return render(request, 'weather/home.html', context)


def get_city_details(request, city_name):
    city = City.objects.get(name=city_name)
    weather_parameters = {
        'q': city.name,
        'appid': weather_api_key,
        'units': 'metric'
    }
    response = requests.get(weather_url, params=weather_parameters)
    data = response.json()
    city_weather = {
        'pk': city.pk,
        'city': city.name,
        'country': data['sys']['country'],
        'temp': round(data['main']['temp'], 1),
        'feels_like': round(data['main']['feels_like'], 1),
        'wind': round(data['wind']['speed']),
        'humidity': data['main']['humidity'],
        'icon': data['weather'][0]['icon'],
        'description': data['weather'][0]['description'].title(),
    }
    context = {'weather_data': city_weather}
    return render(request, 'weather/city_detail.html', context)


class CityDeleteView(DeleteView):
    model = City
    template_name = 'weather/delete_city.html'
    success_url = reverse_lazy('home')
