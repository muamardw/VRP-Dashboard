#!/usr/bin/env python3
"""
🌤️ OpenWeatherMap API Dataset Generator
Generate dataset dengan variabel yang diminta untuk 14 Agustus 2025
"""

import csv
from datetime import datetime, timedelta
import json

# Data simulasi dari OpenWeatherMap API untuk Jakarta, 14 Agustus 2025
# Data ini merepresentasikan forecast 3-hour intervals
WEATHER_DATA = {
    "city": {
        "name": "Jakarta",
        "country": "ID",
        "coord": {"lat": -6.2146, "lon": 106.8451}
    },
    "list": [
        {
            "dt": 1755126000,  # 00:00 WIB
            "main": {
                "temp": 28.5,
                "feels_like": 32.1,
                "pressure": 1010,
                "humidity": 78
            },
            "weather": [{"main": "Clouds"}],
            "clouds": {"all": 85},
            "wind": {
                "speed": 1.2,
                "deg": 180,
                "gust": 2.1
            },
            "visibility": 8000,
            "rain": {"1h": 0.0},
            "dt_txt": "2025-08-14 00:00:00"
        },
        {
            "dt": 1755136800,  # 03:00 WIB
            "main": {
                "temp": 27.8,
                "feels_like": 31.5,
                "pressure": 1009,
                "humidity": 82
            },
            "weather": [{"main": "Rain"}],
            "clouds": {"all": 95},
            "wind": {
                "speed": 0.8,
                "deg": 200,
                "gust": 1.5
            },
            "visibility": 6000,
            "rain": {"1h": 1.2},
            "dt_txt": "2025-08-14 03:00:00"
        },
        {
            "dt": 1755147600,  # 06:00 WIB
            "main": {
                "temp": 27.2,
                "feels_like": 30.8,
                "pressure": 1008,
                "humidity": 85
            },
            "weather": [{"main": "Rain"}],
            "clouds": {"all": 100},
            "wind": {
                "speed": 1.0,
                "deg": 220,
                "gust": 1.8
            },
            "visibility": 5000,
            "rain": {"1h": 2.5},
            "dt_txt": "2025-08-14 06:00:00"
        },
        {
            "dt": 1755158400,  # 09:00 WIB
            "main": {
                "temp": 29.1,
                "feels_like": 33.2,
                "pressure": 1010,
                "humidity": 70
            },
            "weather": [{"main": "Clouds"}],
            "clouds": {"all": 75},
            "wind": {
                "speed": 2.1,
                "deg": 150,
                "gust": 3.2
            },
            "visibility": 9000,
            "rain": {"1h": 0.0},
            "dt_txt": "2025-08-14 09:00:00"
        },
        {
            "dt": 1755169200,  # 12:00 WIB
            "main": {
                "temp": 31.8,
                "feels_like": 36.5,
                "pressure": 1009,
                "humidity": 65
            },
            "weather": [{"main": "Clear"}],
            "clouds": {"all": 25},
            "wind": {
                "speed": 2.8,
                "deg": 120,
                "gust": 4.1
            },
            "visibility": 10000,
            "rain": {"1h": 0.0},
            "dt_txt": "2025-08-14 12:00:00"
        },
        {
            "dt": 1755180000,  # 15:00 WIB
            "main": {
                "temp": 32.4,
                "feels_like": 37.1,
                "pressure": 1008,
                "humidity": 60
            },
            "weather": [{"main": "Clear"}],
            "clouds": {"all": 20},
            "wind": {
                "speed": 3.2,
                "deg": 100,
                "gust": 4.8
            },
            "visibility": 10000,
            "rain": {"1h": 0.0},
            "dt_txt": "2025-08-14 15:00:00"
        },
        {
            "dt": 1755190800,  # 18:00 WIB
            "main": {
                "temp": 30.2,
                "feels_like": 34.8,
                "pressure": 1010,
                "humidity": 75
            },
            "weather": [{"main": "Clouds"}],
            "clouds": {"all": 80},
            "wind": {
                "speed": 2.5,
                "deg": 160,
                "gust": 3.9
            },
            "visibility": 8500,
            "rain": {"1h": 0.0},
            "dt_txt": "2025-08-14 18:00:00"
        },
        {
            "dt": 1755201600,  # 21:00 WIB
            "main": {
                "temp": 28.9,
                "feels_like": 32.6,
                "pressure": 1011,
                "humidity": 80
            },
            "weather": [{"main": "Rain"}],
            "clouds": {"all": 90},
            "wind": {
                "speed": 1.8,
                "deg": 190,
                "gust": 2.7
            },
            "visibility": 7000,
            "rain": {"1h": 0.8},
            "dt_txt": "2025-08-14 21:00:00"
        }
    ]
}

def generate_openweathermap_dataset():
    """Generate dataset OpenWeatherMap dengan variabel yang diminta"""
    
    # Buat file CSV
    filename = 'openweathermap_dataset_14august2025.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'timestamp', 'time_wib', 'temp', 'feels_like', 'pressure', 
            'humidity', 'visibility', 'wind_speed', 'wind_deg', 'wind_gust',
            'rain_1h', 'clouds_all', 'weather_main'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in WEATHER_DATA['list']:
            # Parse timestamp
            dt = datetime.fromtimestamp(item['dt'])
            time_wib = dt.strftime('%H:%M WIB')
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Extract data
            writer.writerow({
                'timestamp': timestamp,
                'time_wib': time_wib,
                'temp': round(item['main']['temp'], 1),
                'feels_like': round(item['main']['feels_like'], 1),
                'pressure': item['main']['pressure'],
                'humidity': item['main']['humidity'],
                'visibility': item.get('visibility', 10000),
                'wind_speed': round(item['wind']['speed'], 1),
                'wind_deg': item['wind']['deg'],
                'wind_gust': round(item['wind'].get('gust', 0), 1),
                'rain_1h': round(item.get('rain', {}).get('1h', 0), 1),
                'clouds_all': item['clouds']['all'],
                'weather_main': item['weather'][0]['main']
            })
    
    print(f"✅ Dataset tersimpan sebagai '{filename}'")
    
    # Tampilkan preview data
    print("\n📊 PREVIEW DATASET:")
    print("=" * 120)
    print(f"{'Waktu':<12} {'Temp':<6} {'Feels':<6} {'Press':<6} {'Hum':<4} {'Vis':<5} {'Wind':<5} {'Deg':<4} {'Gust':<5} {'Rain':<5} {'Cloud':<6} {'Weather':<10}")
    print("-" * 120)
    
    for item in WEATHER_DATA['list']:
        dt = datetime.fromtimestamp(item['dt'])
        time_wib = dt.strftime('%H:%M')
        
        print(f"{time_wib:<12} {item['main']['temp']:<6.1f} {item['main']['feels_like']:<6.1f} {item['main']['pressure']:<6} {item['main']['humidity']:<4} {item.get('visibility', 10000):<5} {item['wind']['speed']:<5.1f} {item['wind']['deg']:<4} {item['wind'].get('gust', 0):<5.1f} {item.get('rain', {}).get('1h', 0):<5.1f} {item['clouds']['all']:<6} {item['weather'][0]['main']:<10}")
    
    # Buat file JSON juga
    json_filename = 'openweathermap_dataset_14august2025.json'
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(WEATHER_DATA, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Dataset JSON tersimpan sebagai '{json_filename}'")
    
    # Statistik dataset
    print("\n📈 STATISTIK DATASET:")
    print("=" * 50)
    
    temps = [item['main']['temp'] for item in WEATHER_DATA['list']]
    humidities = [item['main']['humidity'] for item in WEATHER_DATA['list']]
    wind_speeds = [item['wind']['speed'] for item in WEATHER_DATA['list']]
    pressures = [item['main']['pressure'] for item in WEATHER_DATA['list']]
    rain_amounts = [item.get('rain', {}).get('1h', 0) for item in WEATHER_DATA['list']]
    
    print(f"Temperatur: {min(temps):.1f}°C - {max(temps):.1f}°C (Rata-rata: {sum(temps)/len(temps):.1f}°C)")
    print(f"Kelembaban: {min(humidities)}% - {max(humidities)}% (Rata-rata: {sum(humidities)/len(humidities):.0f}%)")
    print(f"Kecepatan Angin: {min(wind_speeds):.1f} - {max(wind_speeds):.1f} m/s (Rata-rata: {sum(wind_speeds)/len(wind_speeds):.1f} m/s)")
    print(f"Tekanan: {min(pressures)} - {max(pressures)} hPa (Rata-rata: {sum(pressures)/len(pressures):.0f} hPa)")
    print(f"Total Curah Hujan: {sum(rain_amounts):.1f} mm")
    
    # Kondisi cuaca
    weather_counts = {}
    for item in WEATHER_DATA['list']:
        weather = item['weather'][0]['main']
        weather_counts[weather] = weather_counts.get(weather, 0) + 1
    
    print(f"\nKondisi Cuaca:")
    for weather, count in weather_counts.items():
        print(f"  {weather}: {count} periode")

def create_detailed_analysis():
    """Buat analisis detail dataset"""
    
    filename = 'openweathermap_analysis_14august2025.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Waktu', 'Temperatur (°C)', 'Temperatur Terasa (°C)', 'Tekanan (hPa)', 
            'Kelembaban (%)', 'Visibilitas (m)', 'Kecepatan Angin (m/s)', 
            'Arah Angin (°)', 'Angin Gust (m/s)', 'Curah Hujan (mm)', 
            'Tutupan Awan (%)', 'Kondisi Cuaca', 'Kategori Suhu', 'Kategori Kelembaban',
            'Kategori Angin', 'Dampak pada Traffic'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in WEATHER_DATA['list']:
            dt = datetime.fromtimestamp(item['dt'])
            time_wib = dt.strftime('%H:%M WIB')
            
            temp = item['main']['temp']
            humidity = item['main']['humidity']
            wind_speed = item['wind']['speed']
            
            # Kategori suhu
            if temp < 20:
                temp_category = "Dingin"
            elif temp < 25:
                temp_category = "Sejuk"
            elif temp < 30:
                temp_category = "Hangat"
            elif temp < 35:
                temp_category = "Panas"
            else:
                temp_category = "Sangat Panas"
            
            # Kategori kelembaban
            if humidity < 30:
                humidity_category = "Sangat Kering"
            elif humidity < 50:
                humidity_category = "Kering"
            elif humidity < 70:
                humidity_category = "Normal"
            elif humidity < 80:
                humidity_category = "Lembab"
            else:
                humidity_category = "Sangat Lembab"
            
            # Kategori angin
            if wind_speed < 0.5:
                wind_category = "Tenang"
                traffic_impact = "Tidak Ada"
            elif wind_speed < 1.5:
                wind_category = "Lemah"
                traffic_impact = "Minimal"
            elif wind_speed < 2.5:
                wind_category = "Sedang"
                traffic_impact = "Sedang"
            elif wind_speed < 4.0:
                wind_category = "Kuat"
                traffic_impact = "Signifikan"
            else:
                wind_category = "Sangat Kuat"
                traffic_impact = "Tinggi"
            
            writer.writerow({
                'Waktu': time_wib,
                'Temperatur (°C)': round(temp, 1),
                'Temperatur Terasa (°C)': round(item['main']['feels_like'], 1),
                'Tekanan (hPa)': item['main']['pressure'],
                'Kelembaban (%)': humidity,
                'Visibilitas (m)': item.get('visibility', 10000),
                'Kecepatan Angin (m/s)': round(wind_speed, 1),
                'Arah Angin (°)': item['wind']['deg'],
                'Angin Gust (m/s)': round(item['wind'].get('gust', 0), 1),
                'Curah Hujan (mm)': round(item.get('rain', {}).get('1h', 0), 1),
                'Tutupan Awan (%)': item['clouds']['all'],
                'Kondisi Cuaca': item['weather'][0]['main'],
                'Kategori Suhu': temp_category,
                'Kategori Kelembaban': humidity_category,
                'Kategori Angin': wind_category,
                'Dampak pada Traffic': traffic_impact
            })
    
    print(f"✅ Analisis detail tersimpan sebagai '{filename}'")

if __name__ == "__main__":
    print("🌤️ OpenWeatherMap API Dataset Generator")
    print("=" * 50)
    print("📅 Tanggal: 14 Agustus 2025")
    print("📍 Lokasi: Jakarta, Indonesia")
    print("⏰ Interval: 3 jam (00:00 - 21:00 WIB)")
    print("=" * 50)
    
    # Generate dataset
    generate_openweathermap_dataset()
    
    # Buat analisis detail
    create_detailed_analysis()
    
    print("\n🎉 Dataset generation selesai!")
    print("\n📁 File yang dihasilkan:")
    print("  - openweathermap_dataset_14august2025.csv (Data mentah)")
    print("  - openweathermap_dataset_14august2025.json (Format JSON)")
    print("  - openweathermap_analysis_14august2025.csv (Analisis detail)")
    
    print("\n💡 Cara menggunakan:")
    print("  1. Buka file CSV di Excel atau aplikasi spreadsheet")
    print("  2. Gunakan untuk analisis VRP dan machine learning")
    print("  3. Data siap untuk training model DQN") 