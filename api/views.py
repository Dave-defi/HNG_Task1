from django.http import JsonResponse
from django.views import View
import requests

IPINFO_TOKEN = '179088c03e316c'
OPENWEATHERMAP_API_KEY = 'e998ec49f58170dd710d71fd0af49bc7'


class HelloView(View):
    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Guest')
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        
        ipinfo_url = f'http://ipinfo.io/{client_ip}?token={IPINFO_TOKEN}'
        location_info = requests.get(ipinfo_url).json()

        city = location_info.get('city')
        loc = location_info.get('loc')

        weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={loc.split(",")[0]}&lon={loc.split(",")[1]}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
        weather_info = requests.get(weather_url).json()
        temperature = weather_info['main']['temp']

        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

        response = {
            'client_ip': client_ip,
            'location': city,
            'greeting': greeting
        }

        return JsonResponse(response)