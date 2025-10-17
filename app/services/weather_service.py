import requests
from flask import current_app
from datetime import datetime, timedelta
import json

class WeatherService:
    def __init__(self):
        self.base_url = current_app.config['WEATHER_API_BASE_URL']
        self.api_key = current_app.config['WEATHER_API_KEY']
    
    def get_current_weather(self, city_name):
        """Get current weather for a city"""
        try:
            url = f"{self.base_url}/current.json"
            params = {
                'key': self.api_key,
                'q': city_name,
                'aqi': 'no'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'location': {
                    'name': data['location']['name'],
                    'country': data['location']['country'],
                    'lat': data['location']['lat'],
                    'lon': data['location']['lon']
                },
                'current': {
                    'temp_c': data['current']['temp_c'],
                    'temp_f': data['current']['temp_f'],
                    'condition': data['current']['condition']['text'],
                    'humidity': data['current']['humidity'],
                    'precip_mm': data['current']['precip_mm'],
                    'wind_kph': data['current']['wind_kph'],
                    'feelslike_c': data['current']['feelslike_c']
                }
            }
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Weather API error: {str(e)}")
            return None
    
    def get_forecast(self, city_name, days=7):
        """Get weather forecast for a city"""
        try:
            url = f"{self.base_url}/forecast.json"
            params = {
                'key': self.api_key,
                'q': city_name,
                'days': days,
                'aqi': 'no',
                'alerts': 'no'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            forecast_data = {
                'location': {
                    'name': data['location']['name'],
                    'country': data['location']['country'],
                    'lat': data['location']['lat'],
                    'lon': data['location']['lon']
                },
                'current': {
                    'temp_c': data['current']['temp_c'],
                    'condition': data['current']['condition']['text'],
                    'humidity': data['current']['humidity'],
                    'precip_mm': data['current']['precip_mm']
                },
                'forecast': []
            }
            
            for day in data['forecast']['forecastday']:
                forecast_data['forecast'].append({
                    'date': day['date'],
                    'max_temp': day['day']['maxtemp_c'],
                    'min_temp': day['day']['mintemp_c'],
                    'avg_temp': day['day']['avgtemp_c'],
                    'max_humidity': day['day']['maxhumidity'],
                    'min_humidity': day['day']['minhumidity'],
                    'total_precip': day['day']['totalprecip_mm'],
                    'condition': day['day']['condition']['text'],
                    'uv_index': day['day']['uv']
                })
            
            return forecast_data
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Weather forecast API error: {str(e)}")
            return None
    
    def search_locations(self, query):
        """Search for locations by name"""
        try:
            url = f"{self.base_url}/search.json"
            params = {
                'key': self.api_key,
                'q': query
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            locations = response.json()
            
            return [{
                'name': loc['name'],
                'country': loc['country'],
                'lat': loc['lat'],
                'lon': loc['lon']
            } for loc in locations]
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Location search API error: {str(e)}")
            return []
    
    def get_climate_data(self, city_name):
        """Get climate information for a city (monthly averages)"""
        try:
            # This would typically require a different endpoint or historical data
            # For now, we'll return basic climate info based on current data
            current_weather = self.get_current_weather(city_name)
            if not current_weather:
                return None
            
            # Mock climate data - in a real app, you'd use historical data
            climate_info = {
                'location': current_weather['location'],
                'climate_zone': self._determine_climate_zone(current_weather),
                'recommended_months': self._get_recommended_months(current_weather),
                'current_season': self._get_current_season()
            }
            
            return climate_info
            
        except Exception as e:
            current_app.logger.error(f"Climate data error: {str(e)}")
            return None
    
    def _determine_climate_zone(self, weather_data):
        """Determine climate zone based on temperature and precipitation"""
        temp = weather_data['current']['temp_c']
        precip = weather_data['current']['precip_mm']
        
        if temp > 25:
            return 'Tropical' if precip > 100 else 'Arid'
        elif temp > 15:
            return 'Temperate'
        else:
            return 'Cold'
    
    def _get_recommended_months(self, weather_data):
        """Get recommended travel months based on climate"""
        # Simplified recommendation logic
        temp = weather_data['current']['temp_c']
        if 18 <= temp <= 28:
            return ['March', 'April', 'May', 'September', 'October']
        else:
            return ['April', 'May', 'June', 'September', 'October']
    
    def _get_current_season(self):
        """Get current season based on month"""
        month = datetime.now().month
        if 3 <= month <= 5:
            return 'Spring'
        elif 6 <= month <= 8:
            return 'Summer'
        elif 9 <= month <= 11:
            return 'Autumn'
        else:
            return 'Winter'
