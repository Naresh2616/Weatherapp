from django.shortcuts import render, redirect
from .form import CityForm
from .models import City
import requests
from django.contrib import messages

def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=6f490dba633d9301078b005073d2ceb3&units=metric'

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            NCity = form.cleaned_data['name']
            CCity = City.objects.filter(name=NCity).count()
            if CCity == 0:
                res = requests.get(url.format(NCity)).json()
                if res['cod'] == 200:
                    form.save()
                    messages.success(request, f"{NCity} added successfully!")
                else:
                    messages.error(request, "City does not exist!")
            else:
                messages.error(request, "City already exists!")

    form = CityForm()
    cities = City.objects.all()
    data = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if res['cod'] == 200:
            city_weather = {
                'city': city.name,
                'temperature': res['main']['temp'],
                'description': res['weather'][0]['description'],
                'country': res['sys']['country'],
                'icon': res['weather'][0]['icon'],
            }
            data.append(city_weather)

    context = {'data': data, 'form': form}
    return render(request, "weatherapp.html", context)

def delete_city(request, city):
    CName = city.capitalize()
    City.objects.filter(name=city).delete()
    messages.success(request, f"{CName} removed successfully!")
    return redirect('home')
