#!/usr/bin/env python3
"""
Script untuk mengambil sampel data cuaca dari OpenWeatherMap API
untuk kota-kota Jabodetabek
"""

import requests
import json
import time
from datetime import datetime
import pandas as pd

class WeatherDataCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # Kota-kota Jabodetabek
        self.cities = {
            'Jakarta': {'lat': -6.2088, 'lon': 106.8456},
            'Bogor': {'lat': -6.5950, 'lon': 106.8167},
            'Tangerang': {'lat': -6.1500, 'lon': 106.7000},
            'Bekasi': {'lat': -6.3000, 'lon': 107.0500},
            'Depok': {'lat': -6.4000, 'lon': 106.8000}
        }
    
    def get_current_weather(self, city_name):
        """Ambil data cuaca saat ini"""
        try:
            city = self.cities[city_name]
            url = f"{self.base_url}/weather"
            
            params = {
                'lat': city['lat'],
                'lon': city['lon'],
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'id'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self.parse_weather_data(data, city_name)
            
        except requests.exceptions.RequestException as e:
            print(f"Error mengambil data untuk {city_name}: {e}")
            return None
    
    def get_forecast(self, city_name):
        """Ambil data forecast 5 hari"""
        try:
            city = self.cities[city_name]
            url = f"{self.base_url}/forecast"
            
            params = {
                'lat': city['lat'],
                'lon': city['lon'],
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'id'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self.parse_forecast_data(data, city_name)
            
        except requests.exceptions.RequestException as e:
            print(f"Error mengambil forecast untuk {city_name}: {e}")
            return None
    
    def parse_weather_data(self, data, city_name):
        """Parse data cuaca saat ini"""
        try:
            weather_info = {
                'city': city_name,
                'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'visibility': data.get('visibility', 'N/A'),
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind'].get('deg', 'N/A'),
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'clouds': data['clouds']['all'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
            }
            return weather_info
        except KeyError as e:
            print(f"Error parsing data untuk {city_name}: {e}")
            return None
    
    def parse_forecast_data(self, data, city_name):
        """Parse data forecast"""
        forecast_list = []
        
        for item in data['list']:
            forecast_info = {
                'city': city_name,
                'timestamp': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'temp_min': item['main']['temp_min'],
                'temp_max': item['main']['temp_max'],
                'pressure': item['main']['pressure'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'wind_deg': item['wind'].get('deg', 'N/A'),
                'weather_main': item['weather'][0]['main'],
                'weather_description': item['weather'][0]['description'],
                'clouds': item['clouds']['all'],
                'pop': item.get('pop', 0)  # Probability of precipitation
            }
            forecast_list.append(forecast_info)
        
        return forecast_list
    
    def collect_all_current_weather(self):
        """Kumpulkan data cuaca saat ini untuk semua kota"""
        print("🌤️ Mengumpulkan data cuaca saat ini untuk Jabodetabek...")
        print("=" * 80)
        
        all_weather_data = []
        
        for city in self.cities.keys():
            print(f"📡 Mengambil data untuk {city}...")
            weather_data = self.get_current_weather(city)
            
            if weather_data:
                all_weather_data.append(weather_data)
                print(f"✅ {city}: {weather_data['temperature']}°C, {weather_data['weather_description']}")
            else:
                print(f"❌ Gagal mengambil data untuk {city}")
            
            # Delay untuk menghindari rate limiting
            time.sleep(1)
        
        return all_weather_data
    
    def save_to_csv(self, data, filename):
        """Simpan data ke CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"💾 Data disimpan ke {filename}")
    
    def save_to_json(self, data, filename):
        """Simpan data ke JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Data disimpan ke {filename}")

def main():
    # API key OpenWeatherMap
    API_KEY = "ec9a1e4e17acbc7681644f5b8f316236"
    
    # Buat collector
    collector = WeatherDataCollector(API_KEY)
    
    # 1. Ambil data cuaca saat ini
    print("🚀 Memulai pengumpulan data cuaca...")
    current_weather = collector.collect_all_current_weather()
    
    if current_weather:
        # Simpan ke file
        collector.save_to_csv(current_weather, 'sample_weather_data_current.csv')
        collector.save_to_json(current_weather, 'sample_weather_data_current.json')
        
        # Tampilkan ringkasan
        print("\n📊 RINGKASAN DATA CUACA SAAT INI:")
        print("=" * 80)
        for weather in current_weather:
            print(f"🌍 {weather['city']}:")
            print(f"   🌡️  Suhu: {weather['temperature']}°C (feels like: {weather['feels_like']}°C)")
            print(f"   💧 Kelembaban: {weather['humidity']}%")
            print(f"   💨 Angin: {weather['wind_speed']} m/s")
            print(f"   ☁️  Awan: {weather['clouds']}%")
            print(f"   👁️  Visibilitas: {weather['visibility']}m")
            print(f"   🌤️  Kondisi: {weather['weather_description']}")
            print()
    
    # 2. Ambil data forecast untuk Jakarta
    print("🔮 Mengambil data forecast 5 hari untuk Jakarta...")
    jakarta_forecast = collector.get_forecast('Jakarta')
    
    if jakarta_forecast:
        collector.save_to_csv(jakarta_forecast, 'sample_weather_forecast_jakarta.csv')
        collector.save_to_json(jakarta_forecast, 'sample_weather_forecast_jakarta.json')
        
        print(f"✅ Forecast Jakarta: {len(jakarta_forecast)} data points")
        print("📅 Sample forecast data:")
        for i, forecast in enumerate(jakarta_forecast[:5]):  # Tampilkan 5 data pertama
            print(f"   {forecast['timestamp']}: {forecast['temperature']}°C, {forecast['weather_description']}")

if __name__ == "__main__":
    main() 