#!/usr/bin/env python3
"""
🌤️ Jakarta Weather Data Visualization
Visualisasi data cuaca Jakarta dari OpenWeatherMap API
Menampilkan setiap variabel yang mempengaruhi cuaca dalam interval 3 jam
"""

from datetime import datetime

# Data dari OpenWeatherMap API response
WEATHER_DATA = {
    "cod": "200",
    "message": 0,
    "cnt": 40,
    "list": [
        {
            "dt": 1755162000,
            "main": {
                "temp": 32.34,
                "feels_like": 35.79,
                "temp_min": 32.34,
                "temp_max": 32.94,
                "pressure": 1010,
                "sea_level": 1010,
                "grnd_level": 1006,
                "humidity": 53,
                "temp_kf": -0.6
            },
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "hujan sedang",
                    "icon": "10d"
                }
            ],
            "clouds": {"all": 51},
            "wind": {"speed": 2.96, "deg": 37, "gust": 3.17},
            "visibility": 9077,
            "pop": 1,
            "rain": {"3h": 4.29},
            "sys": {"pod": "d"},
            "dt_txt": "2025-08-14 09:00:00"
        },
        {
            "dt": 1755172800,
            "main": {
                "temp": 31.57,
                "feels_like": 38.18,
                "temp_min": 31.34,
                "temp_max": 31.57,
                "pressure": 1010,
                "sea_level": 1010,
                "grnd_level": 1007,
                "humidity": 67,
                "temp_kf": 0.23
            },
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "hujan sedang",
                    "icon": "10n"
                }
            ],
            "clouds": {"all": 65},
            "wind": {"speed": 2.33, "deg": 87, "gust": 3.74},
            "visibility": 6307,
            "pop": 1,
            "rain": {"3h": 4.75},
            "sys": {"pod": "n"},
            "dt_txt": "2025-08-14 12:00:00"
        },
        {
            "dt": 1755183600,
            "main": {
                "temp": 30.44,
                "feels_like": 37.44,
                "temp_min": 30.44,
                "temp_max": 30.44,
                "pressure": 1011,
                "sea_level": 1011,
                "grnd_level": 1008,
                "humidity": 80,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10n"
                }
            ],
            "clouds": {"all": 93},
            "wind": {"speed": 0.84, "deg": 158, "gust": 1.75},
            "visibility": 10000,
            "pop": 1,
            "rain": {"3h": 2.13},
            "sys": {"pod": "n"},
            "dt_txt": "2025-08-14 15:00:00"
        },
        {
            "dt": 1755194400,
            "main": {
                "temp": 27.61,
                "feels_like": 31.41,
                "temp_min": 27.61,
                "temp_max": 27.61,
                "pressure": 1010,
                "sea_level": 1010,
                "grnd_level": 1007,
                "humidity": 82,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10n"
                }
            ],
            "clouds": {"all": 98},
            "wind": {"speed": 1.34, "deg": 231, "gust": 2.29},
            "visibility": 10000,
            "pop": 1,
            "rain": {"3h": 0.54},
            "sys": {"pod": "n"},
            "dt_txt": "2025-08-14 18:00:00"
        },
        {
            "dt": 1755205200,
            "main": {
                "temp": 28.03,
                "feels_like": 32.82,
                "temp_min": 28.03,
                "temp_max": 28.03,
                "pressure": 1009,
                "sea_level": 1009,
                "grnd_level": 1006,
                "humidity": 84,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10n"
                }
            ],
            "clouds": {"all": 100},
            "wind": {"speed": 2.2, "deg": 223, "gust": 3.53},
            "visibility": 10000,
            "pop": 0.86,
            "rain": {"3h": 0.77},
            "sys": {"pod": "n"},
            "dt_txt": "2025-08-14 21:00:00"
        },
        {
            "dt": 1755216000,
            "main": {
                "temp": 28.47,
                "feels_like": 33.87,
                "temp_min": 28.47,
                "temp_max": 28.47,
                "pressure": 1010,
                "sea_level": 1010,
                "grnd_level": 1007,
                "humidity": 83,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10d"
                }
            ],
            "clouds": {"all": 97},
            "wind": {"speed": 1.88, "deg": 195, "gust": 2.86},
            "visibility": 10000,
            "pop": 0.64,
            "rain": {"3h": 0.18},
            "sys": {"pod": "d"},
            "dt_txt": "2025-08-15 00:00:00"
        },
        {
            "dt": 1755226800,
            "main": {
                "temp": 28.79,
                "feels_like": 31.44,
                "temp_min": 28.79,
                "temp_max": 28.79,
                "pressure": 1011,
                "sea_level": 1011,
                "grnd_level": 1007,
                "humidity": 65,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "awan pecah",
                    "icon": "04d"
                }
            ],
            "clouds": {"all": 60},
            "wind": {"speed": 0.78, "deg": 199, "gust": 0.97},
            "visibility": 10000,
            "pop": 0,
            "sys": {"pod": "d"},
            "dt_txt": "2025-08-15 03:00:00"
        },
        {
            "dt": 1755237600,
            "main": {
                "temp": 30.27,
                "feels_like": 33.35,
                "temp_min": 30.27,
                "temp_max": 30.27,
                "pressure": 1008,
                "sea_level": 1008,
                "grnd_level": 1005,
                "humidity": 60,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10d"
                }
            ],
            "clouds": {"all": 69},
            "wind": {"speed": 2.8, "deg": 355, "gust": 1.82},
            "visibility": 10000,
            "pop": 0.26,
            "rain": {"3h": 0.21},
            "sys": {"pod": "d"},
            "dt_txt": "2025-08-15 06:00:00"
        }
    ],
    "city": {
        "id": 1642911,
        "name": "Jakarta",
        "coord": {"lat": -6.2146, "lon": 106.8451},
        "country": "ID",
        "population": 8540121,
        "timezone": 25200,
        "sunrise": 1755126025,
        "sunset": 1755168870
    }
}

class JakartaWeatherVisualizer:
    def __init__(self):
        self.weather_impact = {
            'clear': 1.0,
            'clouds': 1.1,
            'rain': 1.3,
            'heavy_rain': 1.5,
            'storm': 1.8,
            'fog': 1.2,
            'windy': 1.1
        }
    
    def parse_weather_data(self, data):
        """Parse data cuaca dari API response"""
        parsed_data = []
        
        for item in data['list']:
            # Parse timestamp
            dt = datetime.fromtimestamp(item['dt'])
            
            # Extract weather data
            weather_info = {
                'datetime': dt,
                'time_str': dt.strftime('%H:%M'),
                'date_str': dt.strftime('%d/%m/%Y'),
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'temp_min': item['main']['temp_min'],
                'temp_max': item['main']['temp_max'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'wind_deg': item['wind']['deg'],
                'wind_gust': item['wind'].get('gust', 0),
                'clouds': item['clouds']['all'],
                'visibility': item.get('visibility', 10000),
                'weather_main': item['weather'][0]['main'],
                'weather_description': item['weather'][0]['description'],
                'pop': item.get('pop', 0),
                'rain_3h': item.get('rain', {}).get('3h', 0) if 'rain' in item else 0
            }
            
            parsed_data.append(weather_info)
        
        return parsed_data
    
    def get_weather_impact_factor(self, weather_main):
        """Hitung weather impact factor"""
        return self.weather_impact.get(weather_main.lower(), 1.0)
    
    def create_main_weather_table(self, weather_data):
        """Buat tabel utama data cuaca"""
        print("\n" + "="*140)
        print("🌤️ JAKARTA WEATHER FORECAST - 24 JAM (INTERVAL 3 JAM)")
        print("="*140)
        print("Data Source: OpenWeatherMap API")
        print("="*140)
        
        # Header utama
        header = (f"{'Waktu':<12} {'Tanggal':<12} {'Suhu':<8} {'Terasa':<8} {'Min':<6} {'Max':<6} "
                 f"{'Kelembaban':<12} {'Tekanan':<10} {'Angin':<8} {'Arah':<6} {'Gust':<6} "
                 f"{'Awan':<6} {'Jarak':<8} {'Hujan':<8} {'Kondisi':<20} {'Impact':<8}")
        print(header)
        print("-" * 140)
        
        # Data rows
        for data in weather_data:
            impact_factor = self.get_weather_impact_factor(data['weather_main'])
            
            row = (f"{data['time_str']:<12} {data['date_str']:<12} "
                  f"{data['temperature']:<8.1f}°C "
                  f"{data['feels_like']:<8.1f}°C "
                  f"{data['temp_min']:<6.1f}°C "
                  f"{data['temp_max']:<6.1f}°C "
                  f"{data['humidity']:<12.0f}% "
                  f"{data['pressure']:<10.0f}hPa "
                  f"{data['wind_speed']:<8.1f}m/s "
                  f"{data['wind_deg']:<6.0f}° "
                  f"{data['wind_gust']:<6.1f}m/s "
                  f"{data['clouds']:<6.0f}% "
                  f"{data['visibility']/1000:<8.1f}km "
                  f"{data['rain_3h']:<8.1f}mm "
                  f"{data['weather_description']:<20} "
                  f"{impact_factor:<8.2f}x")
            print(row)
        
        print("-" * 140)
    
    def create_detailed_variable_analysis(self, weather_data):
        """Analisis detail setiap variabel cuaca"""
        print("\n" + "="*100)
        print("📊 ANALISIS DETAIL SETIAP VARIABEL CUACA JAKARTA")
        print("="*100)
        
        # 1. Temperature Analysis
        print("\n🌡️ ANALISIS TEMPERATUR:")
        print("-" * 50)
        temps = [data['temperature'] for data in weather_data]
        feels = [data['feels_like'] for data in weather_data]
        temp_mins = [data['temp_min'] for data in weather_data]
        temp_maxs = [data['temp_max'] for data in weather_data]
        
        print(f"Temperatur Aktual:")
        print(f"  - Rata-rata: {sum(temps)/len(temps):.1f}°C")
        print(f"  - Tertinggi: {max(temps):.1f}°C (pukul {weather_data[temps.index(max(temps))]['time_str']})")
        print(f"  - Terendah: {min(temps):.1f}°C (pukul {weather_data[temps.index(min(temps))]['time_str']})")
        print(f"  - Range: {max(temps) - min(temps):.1f}°C")
        
        print(f"\nTemperatur Terasa (Feels Like):")
        print(f"  - Rata-rata: {sum(feels)/len(feels):.1f}°C")
        print(f"  - Tertinggi: {max(feels):.1f}°C")
        print(f"  - Terendah: {min(feels):.1f}°C")
        print(f"  - Selisih terbesar dengan suhu aktual: {max(feels) - max(temps):.1f}°C")
        
        print(f"\nTemperatur Min-Max:")
        print(f"  - Min rata-rata: {sum(temp_mins)/len(temp_mins):.1f}°C")
        print(f"  - Max rata-rata: {sum(temp_maxs)/len(temp_maxs):.1f}°C")
        
        # 2. Humidity Analysis
        print("\n💧 ANALISIS KELEMBABAN:")
        print("-" * 50)
        humidities = [data['humidity'] for data in weather_data]
        
        print(f"Kelembaban Relatif:")
        print(f"  - Rata-rata: {sum(humidities)/len(humidities):.0f}%")
        print(f"  - Tertinggi: {max(humidities):.0f}% (pukul {weather_data[humidities.index(max(humidities))]['time_str']})")
        print(f"  - Terendah: {min(humidities):.0f}% (pukul {weather_data[humidities.index(min(humidities))]['time_str']})")
        print(f"  - Range: {max(humidities) - min(humidities):.0f}%")
        
        # Analisis dampak kelembaban
        high_humidity_count = sum(1 for h in humidities if h > 80)
        print(f"  - Periode kelembaban tinggi (>80%): {high_humidity_count} dari {len(humidities)} periode")
        
        # 3. Wind Analysis
        print("\n💨 ANALISIS ANGIN:")
        print("-" * 50)
        wind_speeds = [data['wind_speed'] for data in weather_data]
        wind_dirs = [data['wind_deg'] for data in weather_data]
        wind_gusts = [data['wind_gust'] for data in weather_data]
        
        print(f"Kecepatan Angin:")
        print(f"  - Rata-rata: {sum(wind_speeds)/len(wind_speeds):.1f} m/s")
        print(f"  - Tertinggi: {max(wind_speeds):.1f} m/s (pukul {weather_data[wind_speeds.index(max(wind_speeds))]['time_str']})")
        print(f"  - Terendah: {min(wind_speeds):.1f} m/s (pukul {weather_data[wind_speeds.index(min(wind_speeds))]['time_str']})")
        
        print(f"\nArah Angin:")
        print(f"  - Range: {min(wind_dirs):.0f}° - {max(wind_dirs):.0f}°")
        print(f"  - Arah dominan: {self.get_wind_direction(sum(wind_dirs)/len(wind_dirs))}")
        
        print(f"\nAngin Gust:")
        print(f"  - Rata-rata: {sum(wind_gusts)/len(wind_gusts):.1f} m/s")
        print(f"  - Tertinggi: {max(wind_gusts):.1f} m/s")
        
        # 4. Pressure Analysis
        print("\n🌪️ ANALISIS TEKANAN UDARA:")
        print("-" * 50)
        pressures = [data['pressure'] for data in weather_data]
        
        print(f"Tekanan Atmosfer:")
        print(f"  - Rata-rata: {sum(pressures)/len(pressures):.0f} hPa")
        print(f"  - Tertinggi: {max(pressures):.0f} hPa (pukul {weather_data[pressures.index(max(pressures))]['time_str']})")
        print(f"  - Terendah: {min(pressures):.0f} hPa (pukul {weather_data[pressures.index(min(pressures))]['time_str']})")
        print(f"  - Range: {max(pressures) - min(pressures):.0f} hPa")
        
        # Analisis tekanan
        high_pressure_count = sum(1 for p in pressures if p > 1013)
        low_pressure_count = sum(1 for p in pressures if p < 1013)
        print(f"  - Periode tekanan tinggi (>1013 hPa): {high_pressure_count} periode")
        print(f"  - Periode tekanan rendah (<1013 hPa): {low_pressure_count} periode")
        
        # 5. Cloud Cover Analysis
        print("\n☁️ ANALISIS TUTUPAN AWAN:")
        print("-" * 50)
        clouds = [data['clouds'] for data in weather_data]
        
        print(f"Tutupan Awan:")
        print(f"  - Rata-rata: {sum(clouds)/len(clouds):.0f}%")
        print(f"  - Tertinggi: {max(clouds):.0f}% (pukul {weather_data[clouds.index(max(clouds))]['time_str']})")
        print(f"  - Terendah: {min(clouds):.0f}% (pukul {weather_data[clouds.index(min(clouds))]['time_str']})")
        
        # Kategorisasi tutupan awan
        clear_sky = sum(1 for c in clouds if c < 25)
        partly_cloudy = sum(1 for c in clouds if 25 <= c < 75)
        mostly_cloudy = sum(1 for c in clouds if c >= 75)
        
        print(f"  - Langit cerah (<25%): {clear_sky} periode")
        print(f"  - Berawan sebagian (25-75%): {partly_cloudy} periode")
        print(f"  - Berawan tebal (≥75%): {mostly_cloudy} periode")
        
        # 6. Visibility Analysis
        print("\n👁️ ANALISIS VISIBILITAS:")
        print("-" * 50)
        visibilities = [data['visibility']/1000 for data in weather_data]
        
        print(f"Jarak Pandang:")
        print(f"  - Rata-rata: {sum(visibilities)/len(visibilities):.1f} km")
        print(f"  - Tertinggi: {max(visibilities):.1f} km")
        print(f"  - Terendah: {min(visibilities):.1f} km")
        
        # Kategorisasi visibilitas
        excellent = sum(1 for v in visibilities if v >= 10)
        good = sum(1 for v in visibilities if 5 <= v < 10)
        moderate = sum(1 for v in visibilities if 2 <= v < 5)
        poor = sum(1 for v in visibilities if v < 2)
        
        print(f"  - Visibilitas sangat baik (≥10 km): {excellent} periode")
        print(f"  - Visibilitas baik (5-10 km): {good} periode")
        print(f"  - Visibilitas sedang (2-5 km): {moderate} periode")
        print(f"  - Visibilitas buruk (<2 km): {poor} periode")
        
        # 7. Precipitation Analysis
        print("\n🌧️ ANALISIS PRESIPITASI:")
        print("-" * 50)
        pops = [data['pop'] * 100 for data in weather_data]
        rains = [data['rain_3h'] for data in weather_data]
        
        print(f"Probabilitas Hujan:")
        print(f"  - Rata-rata: {sum(pops)/len(pops):.0f}%")
        print(f"  - Tertinggi: {max(pops):.0f}%")
        print(f"  - Terendah: {min(pops):.0f}%")
        
        print(f"\nCurah Hujan (3 jam):")
        print(f"  - Total: {sum(rains):.1f} mm")
        print(f"  - Rata-rata: {sum(rains)/len(rains):.1f} mm")
        print(f"  - Tertinggi: {max(rains):.1f} mm (pukul {weather_data[rains.index(max(rains))]['time_str']})")
        
        # Kategorisasi hujan
        no_rain = sum(1 for r in rains if r == 0)
        light_rain = sum(1 for r in rains if 0 < r <= 2.5)
        moderate_rain = sum(1 for r in rains if 2.5 < r <= 7.5)
        heavy_rain = sum(1 for r in rains if r > 7.5)
        
        print(f"  - Tidak hujan: {no_rain} periode")
        print(f"  - Hujan ringan (0-2.5 mm): {light_rain} periode")
        print(f"  - Hujan sedang (2.5-7.5 mm): {moderate_rain} periode")
        print(f"  - Hujan lebat (>7.5 mm): {heavy_rain} periode")
        
        # 8. Weather Conditions Summary
        print("\n☁️ RINGKASAN KONDISI CUACA:")
        print("-" * 50)
        conditions = {}
        for data in weather_data:
            desc = data['weather_description']
            conditions[desc] = conditions.get(desc, 0) + 1
        
        print("Kondisi cuaca yang terjadi:")
        for condition, count in conditions.items():
            percentage = (count / len(weather_data)) * 100
            print(f"  - {condition}: {count} kali ({percentage:.1f}%)")
        
        # 9. Weather Impact Analysis
        print("\n⚡ ANALISIS DAMPAK CUACA PADA TRAFFIC:")
        print("-" * 50)
        impacts = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        
        print(f"Weather Impact Factor:")
        print(f"  - Rata-rata: {sum(impacts)/len(impacts):.2f}x")
        print(f"  - Tertinggi: {max(impacts):.2f}x")
        print(f"  - Terendah: {min(impacts):.2f}x")
        
        # Kategorisasi dampak
        low_impact = sum(1 for i in impacts if i <= 1.1)
        medium_impact = sum(1 for i in impacts if 1.1 < i <= 1.3)
        high_impact = sum(1 for i in impacts if i > 1.3)
        
        print(f"  - Dampak rendah (≤1.1x): {low_impact} periode")
        print(f"  - Dampak sedang (1.1-1.3x): {medium_impact} periode")
        print(f"  - Dampak tinggi (>1.3x): {high_impact} periode")
    
    def get_wind_direction(self, degrees):
        """Konversi derajat ke arah angin"""
        directions = ['Utara', 'Timur Laut', 'Timur', 'Tenggara', 'Selatan', 'Barat Daya', 'Barat', 'Barat Laut']
        index = round(degrees / 45) % 8
        return directions[index]
    
    def create_traffic_impact_table(self, weather_data):
        """Tabel dampak cuaca pada traffic"""
        print("\n" + "="*100)
        print("🚛 DAMPAK CUACA PADA SISTEM VRP JAKARTA")
        print("="*100)
        
        # Header
        header = f"{'Waktu':<12} {'Kondisi':<20} {'Impact':<8} {'Waktu Normal':<12} {'Waktu Terpengaruh':<15} {'Penambahan':<12} {'Rekomendasi':<25}"
        print(header)
        print("-" * 100)
        
        for data in weather_data:
            impact_factor = self.get_weather_impact_factor(data['weather_main'])
            
            # Simulate base travel time (30 minutes for Jakarta routes)
            base_time = 30  # minutes
            impacted_time = base_time * impact_factor
            additional_time = impacted_time - base_time
            
            # Traffic recommendations
            if impact_factor <= 1.1:
                recommendation = "✅ Rute normal"
            elif impact_factor <= 1.3:
                recommendation = "⚠️ Rute alternatif"
            else:
                recommendation = "🚨 Rute alternatif wajib"
            
            row = (f"{data['time_str']:<12} "
                  f"{data['weather_description']:<20} "
                  f"{impact_factor:<8.2f}x "
                  f"{base_time:<12.0f} menit "
                  f"{impacted_time:<15.1f} menit "
                  f"{additional_time:<12.1f} menit "
                  f"{recommendation:<25}")
            print(row)
        
        print("-" * 100)
    
    def create_ascii_charts(self, weather_data):
        """Buat chart ASCII untuk visualisasi"""
        print("\n" + "="*100)
        print("📈 GRAFIK CUACA JAKARTA (ASCII)")
        print("="*100)
        
        # Temperature Chart
        print("\n🌡️ GRAFIK TEMPERATUR:")
        print("-" * 60)
        temps = [data['temperature'] for data in weather_data]
        times = [data['time_str'] for data in weather_data]
        
        max_temp = max(temps)
        min_temp = min(temps)
        temp_range = max_temp - min_temp
        
        print(f"Temperatur: {min_temp:.1f}°C - {max_temp:.1f}°C")
        print()
        
        for i, (temp, time) in enumerate(zip(temps, times)):
            normalized = int(((temp - min_temp) / temp_range) * 40) if temp_range > 0 else 20
            bar = "█" * normalized
            print(f"{time:>8} | {bar:<40} | {temp:>5.1f}°C")
        
        # Humidity Chart
        print("\n💧 GRAFIK KELEMBABAN:")
        print("-" * 60)
        humidities = [data['humidity'] for data in weather_data]
        
        for i, (hum, time) in enumerate(zip(humidities, times)):
            normalized = int((hum / 100) * 40)
            bar = "█" * normalized
            print(f"{time:>8} | {bar:<40} | {hum:>5.0f}%")
        
        # Wind Speed Chart
        print("\n💨 GRAFIK KECEPATAN ANGIN:")
        print("-" * 60)
        wind_speeds = [data['wind_speed'] for data in weather_data]
        max_wind = max(wind_speeds)
        
        for i, (wind, time) in enumerate(zip(wind_speeds, times)):
            normalized = int((wind / max_wind) * 40) if max_wind > 0 else 0
            bar = "█" * normalized
            print(f"{time:>8} | {bar:<40} | {wind:>5.1f} m/s")
        
        # Cloud Cover Chart
        print("\n☁️ GRAFIK TUTUPAN AWAN:")
        print("-" * 60)
        clouds = [data['clouds'] for data in weather_data]
        
        for i, (cloud, time) in enumerate(zip(clouds, times)):
            normalized = int((cloud / 100) * 40)
            bar = "█" * normalized
            print(f"{time:>8} | {bar:<40} | {cloud:>5.0f}%")
    
    def save_to_csv(self, weather_data):
        """Simpan data ke CSV"""
        try:
            # Create CSV content
            csv_content = "Waktu,Tanggal,Temperatur_C,Terasa_C,Temp_Min_C,Temp_Max_C,Kelembaban_Persen,Tekanan_hPa,Kecepatan_Angin_ms,Arah_Angin_Derajat,Angin_Gust_ms,Tutupan_Awan_Persen,Visibilitas_km,Probabilitas_Hujan_Persen,Curah_Hujan_3h_mm,Kondisi_Cuaca,Weather_Impact_Factor\n"
            
            for data in weather_data:
                impact_factor = self.get_weather_impact_factor(data['weather_main'])
                row = (f"{data['time_str']},{data['date_str']},{data['temperature']:.1f},"
                      f"{data['feels_like']:.1f},{data['temp_min']:.1f},{data['temp_max']:.1f},"
                      f"{data['humidity']:.0f},{data['pressure']:.0f},{data['wind_speed']:.1f},"
                      f"{data['wind_deg']:.0f},{data['wind_gust']:.1f},{data['clouds']:.0f},"
                      f"{data['visibility']/1000:.1f},{data['pop']*100:.0f},{data['rain_3h']:.1f},"
                      f"{data['weather_description']},{impact_factor:.2f}")
                csv_content += row + "\n"
            
            # Save to file
            with open('jakarta_weather_visualization.csv', 'w', encoding='utf-8') as f:
                f.write(csv_content)
            
            print(f"\n✅ Data tersimpan ke 'jakarta_weather_visualization.csv'")
            
        except Exception as e:
            print(f"\n⚠️ Error saving CSV: {e}")

def main():
    """Main function"""
    print("🌤️ Jakarta Weather Data Visualization")
    print("="*60)
    
    # Initialize visualizer
    visualizer = JakartaWeatherVisualizer()
    
    # Parse weather data
    print("🔍 Parsing weather data...")
    weather_data = visualizer.parse_weather_data(WEATHER_DATA)
    
    if not weather_data:
        print("❌ Failed to parse weather data")
        return
    
    # Create main weather table
    visualizer.create_main_weather_table(weather_data)
    
    # Create detailed variable analysis
    visualizer.create_detailed_variable_analysis(weather_data)
    
    # Create traffic impact table
    visualizer.create_traffic_impact_table(weather_data)
    
    # Create ASCII charts
    visualizer.create_ascii_charts(weather_data)
    
    # Save to CSV
    visualizer.save_to_csv(weather_data)
    
    print("\n🎉 Jakarta weather visualization completed!")
    print("📁 Generated files:")
    print("  - jakarta_weather_visualization.csv")

if __name__ == "__main__":
    main() 