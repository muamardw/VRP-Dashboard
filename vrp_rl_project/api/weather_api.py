import requests
import os
from utils import load_config, load_env_vars
from typing import Dict, Optional

class WeatherAPI:
    def __init__(self):
        """Initialize Weather API client."""
        self.config = load_config()
        self.env_vars = load_env_vars()
        self.api_key = self.env_vars['OPENWEATHER_API_KEY']
        self.base_url = self.config['api']['openweather']['base_url']
        self.weather_endpoint = self.config['api']['openweather']['weather_endpoint']

    def get_weather(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get current weather conditions for a location.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing weather information or None if request fails
        """
        try:
            url = f"{self.base_url}{self.weather_endpoint}"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'condition': data['weather'][0]['main'].lower(),
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all']
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_weather_impact(self, lat: float, lon: float) -> float:
        """
        Calculate weather impact factor for a location.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Weather impact factor (1.0 for normal conditions)
        """
        weather_data = self.get_weather(lat, lon)
        if weather_data:
            return self.config['weather_impact'].get(
                weather_data['condition'], 
                1.0
            )
        return 1.0  # Default to normal conditions if API fails 