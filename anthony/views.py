from django.shortcuts import render, redirect
import requests

from .models import City
from .forms import CityForm


# Create your views here.

def index(request):
   url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=078d2caaa94f4fe156d5f41f300e9f93'
   error_message = ''
   message = ''
   message_class = ''

   if request.method == 'POST':
      form = CityForm(request.POST)
      if form.is_valid():
         new_city = form.cleaned_data['name']
         if City.objects.filter(name=new_city).count() == 0:
            r = requests.get(url.format(new_city)).json()
            if r['cod'] == 200:
               form.save()
            else:
               error_message = "City doesn't exist in the world!"
         else:
            error_message = "That city already exists!"
      if error_message:
         message = error_message
         message_class = 'is-danger'
      else:
         message = "City added successfully"
         message_class = 'is-success'

   form = CityForm()

   weather_data = []
   cities = City.objects.all()

   for city in cities:
      r = requests.get(url.format(city.name)).json()
      city_weather = {
         'city': city.name,
         'temperature': r['main']['temp'],
         'description': r['weather'][0]['description'],
         'icon': r['weather'][0]['icon'],
      }
      weather_data.append(city_weather)

   context = {'weather_data': weather_data, 'form': form, 'message_class': message_class, 'message': message}
   return render(request, 'wheather.html', context)


def delete_city(request, city_name):
   City.objects.get(name=city_name).delete()
   return redirect('home')